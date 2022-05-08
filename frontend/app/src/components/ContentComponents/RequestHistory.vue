<template>
  <el-containter>
    <el-table
      :data="tableData"
      style="width:900px"
      row-key="id"
      border
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="referring_expression" label="Referring Expression" />
      <el-table-column prop="result" label="Result" />
      <el-table-column prop="image" label="Image URL" />
    </el-table>
  </el-containter>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
const URL_PREFIX_LOCAL = 'http://127.0.0.1:8000/';
const URL_PREFIX_REMOTE = 'http://region-11.autodl.com:13142/';
const URL = URL_PREFIX_LOCAL;
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
// Optionally the request above could also be done as
var tableData = ref<REC[]>([])
axios.get(URL + 'recs/')
  .then(function (response) {
    const recs = response.data
    axios.get(URL + 'imgs/')
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
          }
          console.log(recs[i].vqas)
          recs[i].children = recs[i].vqas
          recs[i].image = img_url_map[recs[i].img]
        }
        tableData.value = recs
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