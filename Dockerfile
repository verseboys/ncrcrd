FROM node:12-slim as assets-builder

ADD package.json /build/package.json
ADD package-lock.json /build/package-lock.json
RUN cd /build \
	&& ADBLOCK=true DISABLE_OPENCOLLECTIVE=true npm install --registry=https://registry.npm.taobao.org --disturl=https://npm.taobao.org/dist \
	&& npm cache clean --force
ENV PATH /build/node_modules/.bin:$PATH

ADD assets /build/assets
ADD webpack.config.js /build/webpack.config.js
RUN cd /build \
	&& webpack --mode production \
	&& find /build/assets/ -type f -name '*.map' -delete

# ---------- 8< ----------

FROM python:3.7-slim

ENV PROJECT_ROOT /project
WORKDIR $PROJECT_ROOT

RUN set -e \
	&& sed -i 's@http://\(security\|deb\).debian.org@http://ftp.cn.debian.org@g' /etc/apt/sources.list \
	&& apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y nginx \
	&& rm -f /etc/nginx/sites-enabled/default \
	&& rm -rf /var/lib/apt/lists/* \
	&& ln -snf /dev/stdout /var/log/nginx/access.log \
	&& ln -snf /dev/stdout /var/log/nginx/error.log

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD requirements.txt $PROJECT_ROOT/
RUN set -e \
	&& sed -i 's@http://\(security\|deb\).debian.org@http://ftp.cn.debian.org@g' /etc/apt/sources.list \
	&& apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
		git libpq5 \
		libpq-dev build-essential python3-dev \
	&& pip3 install --no-cache-dir -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple -r requirements.txt \
	&& apt-get purge -y --auto-remove \
		libpq-dev build-essential python3-dev \
	&& rm -rf /var/lib/apt/lists/*

ADD . $PROJECT_ROOT
COPY --from=assets-builder /build/build /project/build
ADD entrypoint.sh /entrypoint.sh
ADD nginx.conf /etc/nginx/conf.d/default.conf
RUN set -x \
	&& cp natureself/settings_local.example.py natureself/settings_local.py \
	&& python3 manage.py collectstatic --noinput \
	&& rm -f natureself/settings_local.py

ENTRYPOINT ["/entrypoint.sh"]
