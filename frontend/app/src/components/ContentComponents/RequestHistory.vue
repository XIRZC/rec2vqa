<template>
  <el-containter>
    <el-breadcrumb :separator-icon="ArrowRight" style="margin-bottom: 10px">
      <el-breadcrumb-item :to="{ name: 'app', params: { mode: 'Request' }}">REC List</el-breadcrumb-item>
      <el-breadcrumb-item >REC Detail</el-breadcrumb-item>
    </el-breadcrumb>
    <el-table
      :data="tableData"
      style="width: 1000px"
      row-key="id"
      stripe
      height="400"
      border
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="referring_expression" label="Referring Expression" />
      <el-table-column prop="result" label="Result" width="350"/>
      <el-table-column prop="image" label="Image URL" width="100">
        <template #default="scope">
          <el-link :href="scope.row.image" type="primary">
            Image Link
          </el-link>
        </template>
      </el-table-column>
      <el-table-column prop="entry" label="VQA Entry" width="120">
        <template #default="scope">
          <el-button 
            v-if="scope.row.vqas == undefined"
            type="text" 
            size="small" 
            @click="detailJump(scope.$index, scope.row)" >
            VQA Detail
          </el-button>
            <!-- v-else-if="scope.row.vqas.length == 0"  -->
          <el-button 
            v-else
            type="text" 
            size="small" 
            @click="detailJump(scope.$index, scope.row)" >
            REC Detail
          </el-button>
      </template>
      </el-table-column>
    </el-table>
  </el-containter>
</template>
<script lang="ts" setup>
import { ArrowRight } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { useStore } from "../../store";
import { computed } from "vue";
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const store = useStore()
const URL = computed(() => store.state.URL_PREFIX)

const axios = require('axios');

interface VQA {
  id: number
  question: string
  answer: string
};
interface REC {
  id: number
  referring_expression: string
  result: string
  image: string
  hasChildren?: boolean
  children?: VQA[]
};
const detailJump = (index: number, row: REC) => {
  // console.log(index, row)
  router.push({ name: 'app', params: { mode: 'RequestDetail' }})
  console.log('ori_row', row)

  store.commit('set_last_rec_post', row)
}
// Optionally the request above could also be done as
var tableData = ref<REC[]>([])
axios.get(URL.value + 'recs/')
  .then(function (response) {
    const recs = response.data
    axios.get(URL.value + 'imgs/')
      .then(function (response) {
        const imgs = response.data
        const img_url_map = {}
        for (let i = 0; i < imgs.length; i++) {
          img_url_map[imgs[i].id] = imgs[i].img
        }
        for (let i = 0; i < recs.length; i++) {
          for (let j = 0; j < recs[i].vqas.length; j++) {
            recs[i].vqas[j].referring_expression = 'Question: ' + recs[i].vqas[j].question
            recs[i].vqas[j].result = 'Answer: ' + recs[i].vqas[j].answer
            recs[i].vqas[j].parent_referring_expression = recs[i].referring_expression
            recs[i].vqas[j].parent_result = recs[i].result
            recs[i].vqas[j].image = img_url_map[recs[i].img]
          }
          recs[i].parent_referring_expression = recs[i].referring_expression
          recs[i].parent_result = recs[i].result
          recs[i].children = recs[i].vqas
          recs[i].image = img_url_map[recs[i].img]
        }
        tableData.value = recs
        store.commit('set_recs', recs)
      })
      .catch(function (error){
        console.log(error)
      })
      .then(function () {
      });
  })
  .catch(function (error) {
    console.log(error);
  })
  .then(function () {
    // always executed
  });  
</script>