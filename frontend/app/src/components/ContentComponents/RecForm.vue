<template>
  <div style="margin: 20px" />
  <el-form
    label-position="top"
    label-width="100px"
    :model="formData"
    style="max-width: 400px"
  >
    <el-form-item label="Referring Expression:">
      <el-contianer direction="horizontal" style="width: 400px">
        <el-input v-model="formData.exp"
         style="max-width: 320px"
         type="textarea"
         autosize
         clearable
         maxlength="80"
         show-word-limit
         placeholder="Please input a referring expression : )"  />
        <el-button type="primary" @click="submitForm(formadataRef)" style="margin-left: 5px"
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
import { reactive, ref } from 'vue'
import type { FormInstance } from 'element-plus'

const formDataRef = ref<FormInstance>()

const formData = reactive({
  exp: '',
  res: '',
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
