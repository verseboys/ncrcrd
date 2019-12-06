<template>
  <div>
    <div id="filter-control" class="d-flex">
      <div class="w-50 d-flex">
        <span class="w-25 text-center">地区</span>
        <v-select class="w-50 select"
          :options="districts"
          v-model="district"
          @input="refreshTable"
          :searchable="false"
          ></v-select>
        <span class="w-25"></span>
      </div>
      <div class="w-50 d-flex">
        <span class="w-25 text-center">医院等级</span>
        <v-select class="w-50 select"
          :options="levels"
          v-model="level"
          @input="refreshTable"
          :searchable="false"
          ></v-select>
        <span class="w-25"></span>
      </div>
    </div>
    <vuetable ref="table" class="block-table"
              api-url="placeholder"
              :http-fetch="getTableData"
              :fields="fields"
              data-path=""
              pagination-path=""
              no-data-template="没有数据"
              ></vuetable>
  </div>
</template>

<script>
import Vuetable from 'vuetable-2/src/components/Vuetable.vue'
import vSelect from 'vue-select/src/components/Select.vue'
import axios from 'axios'
import _ from 'lodash'

export default {
  name: 'TableCorporation',
  components: {
    Vuetable,
    vSelect,
  },
  props: {
    blockId: {
      type: String,
      required: true,
    },
  },
  data () {
    return {
      blockData: null,

      // vuetable-2 不支持动态更新 fields，因此只能在代码里写死，
      // 不过由于这个表格是单独使用的，所以写死也没有问题
      fields: [
        { name: 'id', title: '序号' },
        { name: 'district', title: '省、市、自治区' },
        { name: 'city', title: '地级市' },
        { name: 'name', title: '单位名称' },
        { name: 'level', title: '医院等级' },
        { name: 'category', title: '类别' },
      ],

      districts: [],
      district: '',
      levels: [],
      level: '',
    }
  },
  methods: {
    getTableData: function (url, options) {
      let vm = this

      if (vm.blockData) { return new Promise(function(resolve, reject) { resolve({data: vm.blockData}) }) }

      return axios.get(`?block=${this.blockId}`)
    },

    // 这个函数名必须是 transform，vuetable-2 会调用这个函数来将服务器返回的数据转化成它需要的数据结构
    transform: function (data) {
      let vm = this
      vm.blockData = data

      if (!data) { return null }

      let rows = data.data.slice(1)

      vm.districts = _.uniq(_.map(rows, (value) => value[1]))
      if (!_.includes(vm.districts, vm.district)) {
        vm.district = '北京'
      }

      vm.levels = _.uniq(_.map(rows, (value) => value[4]))
      if (!_.includes(vm.levels, vm.level)) {
        vm.level = '三甲'
      }

      rows = _.filter(rows, (value) => value[1] === vm.district && value[4] === vm.level)
      return _.map(rows, (value) => _.zipObject(['id', 'district', 'city', 'name', 'level', 'category'], value))
    },

    refreshTable: function () {
      this.$refs.table.refresh()
    },
  },
}
</script>

<style scoped>
#filter-control {
  margin: 20px 10px;
}

.text-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.select /deep/ button.clear {
  display: none;
}

.select /deep/ .dropdown-toggle {
  /* make control looks flat */
  border-radius: 0;
}

.select /deep/ .dropdown-toggle::after {
  border: 0;
}
</style>
