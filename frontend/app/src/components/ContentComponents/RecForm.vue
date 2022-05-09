<template>
  <div style="margin: 20px" />
  <el-form
    label-position="top"
    label-width="100px"
    :model="formData"
    style="max-width: 400px"
  >
  <div style="font-size: 15px; font-weight: bold">
    Step 1: Referring Expression Comprehension (REC)
  </div>
    <el-form-item label="Referring Expression:">
      <el-contianer direction="horizontal" style="width: 400px">
        <el-input v-model="formData.referring_expression"
         style="max-width: 320px"
         type="textarea"
         autosize
         clearable
         maxlength="80"
         show-word-limit
         placeholder="Please input a referring expression : )"  />
        <el-button v-if="!has_rec_posted" type="primary" @click="onSubmit" style="margin-left: 5px"
          >Submit</el-button
        >
      </el-contianer>
    </el-form-item>
    <el-form-item label="Detection Results:">
      <el-input v-model="formData.res" disabled />
    </el-form-item>
  </el-form>
</template>


<script lang="ts" setup>
import { useStore } from "../../store";
import { computed } from "vue";
import { reactive, ref } from 'vue'
const store = useStore()
const URL = computed(() => store.state.URL_PREFIX)
const has_rec_posted = computed(() => store.state.has_rec_posted)
const show_img_id = computed(() => store.state.show_img.id)
const axios = require('axios');

// do not use same name with ref
const formData = reactive({
  referring_expression: '',
  res: '',
  img: 0,
})

const onSubmit = () => {
  formData.img = show_img_id.value
  console.log('rec submit!', formData)
  axios.post(URL.value + 'recs/', formData)
    .then( (response) => {
      // console.log(response);
      store.commit('set_last_rec_post', response)
    })
    .catch( (error) => {
      console.log(error);
    })
    .then( () => {
    })
  store.commit('set_has_rec_posted', {
    bin: true,
  });
}
</script>