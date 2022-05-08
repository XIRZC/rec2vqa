<template>
  <div style="margin: 10px" />
  <el-form
    label-position="top"
    label-width="100px"
    :model="formData"
    style="max-width: 400px"
  >
    <div style="font-size: 15px; font-weight: bold">
      Step 2: Visual Question Answering (VQA)
    </div>
    <el-form-item label="Question:">
      <el-contianer direction="horizontal" style="width: 400px">
        <el-input v-model="formData.question"
         type="textarea"
         style="max-width: 320px"
         autosize
         clearable
         maxlength="80"
         show-word-limit
         placeholder="Please input a question : )"  />
        <el-button type="primary" @click="onSubmit" style="margin-left: 5px"
          >Submit</el-button
        >
      </el-contianer>
    </el-form-item>
    <el-form-item label="Answer:">
      <el-input v-model="formData.answer" disabled />
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { useStore } from "../../store";
import { computed } from "vue";
import { reactive, ref } from 'vue'
const store = useStore()
const last_posted_rec_id = computed(() => store.state.last_rec_post.id)
const URL_PREFIX_LOCAL = 'http://127.0.0.1:8000/';
const URL_PREFIX_REMOTE = 'http://region-11.autodl.com:13142/';
const URL = URL_PREFIX_LOCAL;
const axios = require('axios');

const formData = reactive({
  question: '',
  answer: '',
  rec: 0,
})

const onSubmit = () => {
  formData.rec = last_posted_rec_id.value
  console.log('vqa submit!', formData)
  axios.post(URL + 'vqas/', formData)
    .then( (response) => {
      console.log(response);
    })
    .catch( (error) => {
      console.log(error);
    })
    .then( () => {
    })
}
</script>
