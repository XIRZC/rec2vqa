<template>
  <el-containter>
    <el-breadcrumb :separator-icon="ArrowRight" style="margin-bottom: 10px">
      <el-breadcrumb-item :to="{ name: 'app', params: { mode: 'Request' }}">{{rec_list_text}}</el-breadcrumb-item>
      <el-breadcrumb-item >{{rec_detail_text}}</el-breadcrumb-item>
    </el-breadcrumb>
    <el-table
      :data="tableData"
      style="width: 1000px"
      row-key="id"
      stripe
      height="400"
      border
    >
      <el-table-column prop="id" :label="table_id_text" width="80" />
      <el-table-column prop="referring_expression" :label="table_re_text" />
      <el-table-column prop="result" :label="table_res_text" width="350"/>
      <el-table-column prop="image" :label="table_image_url_text" width="100">
        <template #default="scope">
          <el-link :href="scope.row.image" type="primary">
            {{table_image_link_text}}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column prop="entry" :label="table_vqa_entry_text" width="120">
        <template #default="scope">
          <el-button 
            v-if="scope.row.vqas == undefined"
            type="text" 
            size="small" 
            @click="detailJump(scope.$index, scope.row)" >
            {{table_vqa_detail_text}}
          </el-button>
            <!-- v-else-if="scope.row.vqas.length == 0"  -->
          <el-button 
            v-else
            type="text" 
            size="small" 
            @click="detailJump(scope.$index, scope.row)" >
            {{rec_detail_text}}
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
import { ElLoading } from 'element-plus'

const router = useRouter()
const route = useRoute()

const store = useStore()
const URL = computed(() => store.state.URL_PREFIX)

const rec_list_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.rec_list )
const rec_detail_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.rec_detail )
const table_id_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_id )
const table_re_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_re )
const table_res_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_res )
const table_image_url_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_image_url )
const table_image_link_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_image_link )
const table_vqa_entry_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_vqa_entry )
const table_vqa_detail_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_vqa_detail )

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
  row.referring_expression = row.referring_expression.replace('Question: ', '')
  row.result = row.result.replace('Answer: ', '')
  console.log('replaced_row', row)

  store.commit('set_last_rec_post', row)
}
// Optionally the request above could also be done as
var tableData = ref<REC[]>([])

const loadingInstance = ElLoading.service({
  lock: true,
  text: 'Loading...',
  background: 'rgba(0, 0, 0, 0.1)',
})
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
            recs[i].vqas[j].result_image = recs[i].result_image
          }
          recs[i].parent_referring_expression = recs[i].referring_expression
          recs[i].parent_result = recs[i].result
          recs[i].children = recs[i].vqas
          recs[i].image = img_url_map[recs[i].img]
        }
        tableData.value = recs
	loadingInstance.close()
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
