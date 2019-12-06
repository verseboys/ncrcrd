<<<<<<< HEAD
# CMS 网站项目

本项目设计为可以被复用，多个网站可以共用同一个项目。

目前已有的网站有：

* **国家呼吸疾病临床研究中心**，National Clinical Research Center for Respiratory Disease，中文简称 *疾病中心*，英文简写为 *NCRCRD*

## 本地开发快速上手

```sh
git clone git@git.evahealth.net:natureself/cms.git
cd cms

# 安装依赖
pip install -r requirements-dev.txt
npm install

# 创建配置文件
cp natureself/settings_local.example.py natureself/settings_local.py
# 打开 settings_local.py 文件，并按照本地需求对文件进行修改

# 如果使用的是一个新建的空数据库，那么请运行一次 migration，如果使用别人创建好的数据库则可以跳过
python ./manage.py migrate

# 为自己创建一个账号
python ./manage.py createsuperuser

# 运行 webpack（这会一直在前台运行，所以下一条命令需要开一个新的终端运行）
./node_modules/.bin/webpack -w

# 运行
python ./manage.py runserver
```

*以下步骤是裸启动步骤*

> 当使用一个之前没有配置过的数据库时，请在创建用户后，登录管理后台（ http://127.0.0.1:8000/admin/ ），
> 为疾病中心站点创建一个首页，然后在 *设置->站点* 中，添加一个站点，配置如下：
> 
> * 主机名：`ncrcrd.localhost`
> * 端口号：`8000`
> * 站点名称：`国家呼吸疾病临床研究中心`
> * 根页面：选择疾病中心的根页面
> * 根据自己的需求勾选“是默认站点” （在生产环境中，默认站点会配置一个空的站点，乱七八糟的域名都会返回404，
>   本地开发时可以根据自己的方便需求随意设定）
> 
> 配置好后，就可以通过 http://ncrcrd.localhost:8000/ 来访问这个站点了。
>
> 以后有多个站点时，都可以通过该方式来配置。

也可以通过加载项目里内置的一些测试数据，快速搭建一个有一定数据量的环境，查看站点效果。具体步骤如下：

```sh
cp -r testdata/media .

# 需要在 autoops 中创建一个 postgres 数据库，不要用 sqlite，sqlite 可能无法导入成功
# 如果是已经存在的数据库，请清空数据库（使用 None 来 reinitialize 数据库）
# 然后运行 migrate
./manage.py migrate

# 接下来导入数据库数据
./manage.py loaddata testdata/testdata.json
```

日常调试时，可以运行以下命令得到一个 ipython shell：

```sh
python ./manage.py shell
```

## 代码结构

本项目使用 wagtail 创建，实质上是一个普通的 Django 项目。项目名（相当于 `django-admin start project $project` 中
`$project` 的值）为 `natureself`。我们以后创建的 Django 项目，原则上项目名都使用 `natureself`。

`search` 为 wagtail 默认创建的一个 app，主要负责搜索的功能。

wagtail 还创建了一个 app，名为 `home`，我们将其删除，并根据我们的情形来创建所需的 app。

我们使用 wagtail 的多站点（multisite）功能，实现一个项目多个站点。wagtail 的多站点功能原理大致如下：
我们可以在 *Settings -> Sites* 中添加多个占地那，一个站点其实就是一个域名，一个站点会关联一个根页面（Root Page），
该站点的所有内容都由这个根页面链接。每一个站点对应一棵页面树（Page Tree），根页面即这个页面树的根节点。

对于每一个站点，我们需要创建三个目录：

* 站点的 app 目录，用于实现站点的 models，以及其他可能需要的 view 之类的内容
* assets/ 中创建子目录，这里面存放该站点用到的静态资源文件（如 js、css、image 等）
* templates/ 中创建子目录，这里面存放该站点各页面的 Django 模板文件

仅与单个站点有关的内容，不得存放在除上述三个目录以外的任何其他地方。简单的说，当我们需要删除一个站点时，
只需要查找所有名为站点名的目录即可，并且不会造成任何其他副作用（当然，settings.py 中需要删除该站点相关的内容）。

整个项目的代码结构如下：

```
/-
 |- natureself/           # 在配置文件中，这个目录为 PROJECT_DIR
    |- settings.py        # 配置文件，公共部分
    |- settings_local.py  # 配置文件，本地使用，不提交到 git 中
    |- settings_local.example.py
    |- static/            # wagtail 默认生成，用于几个全局默认页面，我们不得向这里面保存东西
    |- templates/         # wagtail 默认生成，用于几个全局默认页面，我们不得向这里面保存东西
    |- ...                # 其他文件我们一般无需关注
 |- search/               # wagtail 默认生成，与搜索功能有关，以后用到时再探索
 |- common/               # 所有站点共用的代码，后面详细说明
    |- models.py
 |- ncrcrd/               # 疾病中心站点的内容，后面详细说明
 |- templates/
    |- ncrcrd/            # 疾病中心站点的模板，后面详细说明
    |- $site/             # 每个站点会在这里创建一个目录
 |- assets/
    |- ncrcrd/            # 疾病中心站点的静态资源，后面详细说明
    |- $site/             # 其他站点的目录
```

# 配置文件规范

Django 的配置文件，习惯上有几种管理方式， wagtail 使用 `dev` + `production` 的方式，即项目中存放一个 `dev.py` 和一个 `production.py`
文件，在本地使用 `dev.py`，在部署时，通过修改 `wsgi.py` 文件来指定使用 `production.py` 。

但这种方式有几个问题：

* 原则上，生产环境使用的配置内容不应该提交到 git 中，尤其是数据库相关的配置
* 使用这种方式，在部署时不仅要部署一个配置文件，还需要额外部署一个 `wsgi.py` 文件，对于部署来说，这是比较有负担的事情
* 每一个开发者在本地可能会使用不同的数据库或其他配置，因此大家共用一个 `dev.py` 并不方便

因此我们使用另一种常见的方式，`settings.py` + `settings_local.py` ，其中：

* `settings.py` 中保存各环境中相同的配置信息，并且不包含任何隐私信息（如数据库账号等）
* `settings_local.py` 中保存各环境（包括用户本地开发环境）中不同的内容。该文件 **不允许**提交到git中。
  我们提供一个 `settings_local.example.py` 文件，这个文件里将所有需要在本地配置的项目列出来，并加上注释，
  每一位开发者本地要开发时，请复制该文件为 `settings_local.py`，并根据自己的情况进行配置。

# 代码结构

每个站点需要使用不同的主题，一个主题可以理解为该站点所有页面类型的模板组成一套模板集合。
在一般的 Django 应用中，模板文件一般放在 app 的目录中，在 `$app/templates/$app/` 这个目录下。

对于公共的部分（包括model、template、静态文件等），我们都放在名为 common 的 app 中，而 template、静态文件
可以使用软链的方式链接到相应站点 app 的目录中。

具体项目的代码结构如下：

```
/-
 |- natureself/
    |- settings.py         # 配置文件，公共部分
    |- settings_local.py   # 配置文件，本地使用，不提交到git中
    |- settings_local.example.py
    |- static/             # wagtail 默认生成，用于几个默认页面，后续将为每个站点单独实现并删除这里
    |- templates/          # wagtail 默认生成，用于几个默认页面，后续将为每个站点单独实现并删除这里
    |- urls.py             # 主路由文件，平时基本无需修改
    |- ...                 # 其他开发者无需关心的文件
 |- search/                # wagtail 默认生成，与搜索有关的功能，稍后再探索
 |- ncrcrd/
    |- models.py           # 疾病中心专有的内容 model
    |- migrations/
    |- templates/ncrcrd/
       |- home_page.html
       |- ...
       |- common_page.html --symlink--> ../../../common/templates/common/common_page.html
    |- static/
       |- ncrcrd/
          |- js/
          |- css/
          |- img/
 |- $another-site/         # 其他站点的 model
    |- models.py
    |- migrations/
    |- templates/
    |- static/
 |- common/
    |- models.py           # 各站点间共享的 model
    |- migrations/
    |- templates/common/
       |- common_page.html
    |- static/
```

## Model 说明

有一些常见的页面 model、block model、field model 等，我们会在各个站点中共享使用。这些 model 我们都在 `common/models.py`
中实现。但是注意，Django 中每一个 model 对应一个数据库表，如果各个站点直接使用 common 中的 model，那么这些站点的数据也都会
存在相同的表中，使得这些数据混杂在一起，如果将来我们需要单独迁移一个站点，会很难分离数据。因此，我们使用另一种方式，
在 `common/models.py` 中只声明 *抽象model* （在 Meta 类中声明 `abstract = True`），然后在各站点的 model 中继承这些类。
这带来的额外好处是，每个站点还可以根据实际需求对公共的 model 进行定制。

关于 Django 中 model 类的继承的说明，请阅读
[Django 官方文档](https://docs.djangoproject.com/en/2.1/topics/db/models/#model-inheritance)
了解更多。

目前 `common/models.py` 中只声明了一个 `GenericPage` ，这个页面类型包含了一个 `StreamField` 用于存放正文部分，可以满足
绝大多数页面的需求。另外有两个开关控制，`show_sidebar` 控制该页面是否显示侧边栏，`show_breadcrumb` 控制该页面是否显示面包屑导航，
这两个开关都默认为 False，在各个站点中可以自行设置默认值，例如在疾病中心站点中，这两个值都设置为了 True。

## Webpack 说明

我们使用 webpack 来打包前端静态资源，主要目的有两个，一个是方便写 js 代码，我们可以使用模块化的方式写 js 的代码，
可以方便的 `import` 第三方库，可以将我们自己的代码分解到多个文件中，也可以写 Vue 的单文件模块（Single File Component,
即 `.vue` 文件）等等。第二个是可以用 scss 来写 css 代码，这使得我们可以方便的用多个文件来组织我们的 css 代码，管理更方便，
并且可以得到许多好处。许多成熟的第三方库（如 bootstrap）也提供了 scss，我们可以 import 它们，并对它们进行定制，
这比我们裸写 css 代码来强制覆盖 bootstrap 中的一些类要方便的多。

`assets/` 目录即为这些静态资源的*源代码*文件，所有 js 代码放在 `assets/$site/js/` 中，入口文件为 `index.js` （具体见 `webpack.config.js`），
目前疾病中心站点中，我引入了 `Vue`，但实际上并没有使用，仅作为演示使用。
在个别页面，我们可以使用 Vue 来简化开发，例如在渲染表格数据时，Vue 可能可以使开发工作变得简单。
在 js 中，我们将所有需要让网页里使用的模块都*挂载*到 `window.modules` 下，这样，在网页的内联 js 里，我们就可以用 `modules.XXX` 来引用了。
`assets/$site/css/` 为所有的 css 文件，其中 `index.scss` 为入口文件。

当我们运行 `webpack` 命令时，webpack 会将这些文件编译生成一个 js 文件和一个 css 文件，文件被保存到 `./build/assets/` 目录下，
注意，这里的 `build/` 目录不能添加到 git 里（已经在 `.gitignore` 中剔除）。生成的文件名为 `$site.$hash.js|css`。
其中 `$site` 为站点缩写，例如 `ncrcrd`，`$hash` 由 webpack 自动生成，每次代码改变后，`$hash` 也会变化，这也带来了额外的好处，
以前我们的 django 站点中，静态文件同名更新后，浏览器往往会由于缓存而无法加载最新的文件。

对于 js、css 以外的文件，例如 `img/` 目录，会被复制到 `./build/assets/` 目录中，不做任何处理。这需要配置 `webpack.config.js` 来实现，
当我们要增加子目录或者需要复制第三方库的一些文件时，需要在 `webpack.config.js` 中找到 `CopyWebpackPlugin` 的段落进行配置。
=======
# ncrcrd
CMS 国家呼吸疾病临床医学研究中心
>>>>>>> 40b01486e229814a46a58458454b7d70285747c1
