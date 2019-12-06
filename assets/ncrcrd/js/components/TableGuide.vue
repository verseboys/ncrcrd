<template>
  <div>
    <div id="filter-control" class="d-flex">
      <div class="w-50 d-flex">
        <span class="w-25 text-center">类别</span>
        <v-select class="w-50 select"
          :options="categories"
          v-model="category"
          @input="refreshTable"
          :searchable="false"
          ></v-select>
        <span class="w-25"></span>
      </div>
      <div class="w-50 d-flex">
        <span class="w-25 text-center">发布年份</span>
        <v-select class="w-50 select"
          :options="publishYears"
          v-model="publishYear"
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
  name: 'TableGuide',
  components: {
    Vuetable,
    vSelect,
  },
  props: {
    blockId: {
      type: String,
      required: true,
    }
  },
  data () {
    return {
      blockData: null,

      // vuetable-2 不支持动态更新 fields，因此只能在代码里写死，
      // 不过由于这个表格是单独使用的，所以写死也没有问题
      fields: [
        { name: 'orgName', title: '依托单位名称' },
        { name: 'title', title: '名称' },
        { name: 'category', title: '类别' },
        { name: 'publishYear', title: '发布年份' },
        { name: 'role', title: '牵头或参与' },
        { name: 'leaderOrg', title: '牵头单位' },
      ],

      categories: [],
      category: '',
      publishYears: [],
      publishYear: '',
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

      vm.categories = _.uniq(_.map(rows, (value) => value[2]))
      vm.categories = _.concat(['全部'], vm.categories)
      if (!vm.category || !_.includes(vm.categories, vm.category)) {
        vm.category = '全部'
      }

      vm.publishYears = _.uniq(_.map(rows, (value) => value[3]))
      vm.publishYears = _.concat(['全部'], _.sortBy(vm.publishYears))
      if (!vm.publishYear || !_.includes(vm.publishYears, vm.publishYear)) {
        vm.publishYear = '全部'
      }

      let filter = function (row, category, publishYear) {
        if (category !== '全部' && row[2] !== category) { return false }
        if (publishYear !== '全部' && row[3] !== publishYear) { return false }
        return true
      }

      rows = _.filter(rows, (value) => filter(value, vm.category, vm.publishYear))
      return _.map(rows, (value) => _.zipObject(['orgName', 'title', 'category', 'publishYear', 'role', 'leaderOrg'], value))
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
