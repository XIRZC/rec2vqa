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
        <el-button type="primary" @click="submitForm(formadataRef)" style="margin-left: 5px"
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
import { reactive, ref } from 'vue'
import type { FormInstance } from 'element-plus'

const formDataRef = ref<FormInstance>()

const formData = reactive({
  question: '',
  answer: '',
})

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      console.log('submit!', fields)
    } else {
      console.log('error submit!', fields)
    }
  })
}
</script>
