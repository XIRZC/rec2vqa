<template>
  <div>
    <el-radio-group v-model="radio1" size="large">
      <el-radio-button label="New York" />
      <el-radio-button label="Washington" />
      <el-radio-button label="Los Angeles" />
      <el-radio-button label="Chicago" />
    </el-radio-group>
  </div>
  <div style="margin-top: 20px">
    <el-radio-group v-model="radio2">
      <el-radio-button label="New York" />
      <el-radio-button label="Washington" />
      <el-radio-button label="Los Angeles" />
      <el-radio-button label="Chicago" />
    </el-radio-group>
  </div>
  <div style="margin-top: 20px">
    <el-radio-group v-model="radio3" size="small">
      <el-radio-button label="New York" />
      <el-radio-button label="Washington" disabled />
      <el-radio-button label="Los Angeles" />
      <el-radio-button label="Chicago" />
    </el-radio-group>
  </div>
  <div style="margin-top: 20px">
      <el-radio-group v-model="mode">
        <el-radio-button label="Main" />
        <el-radio-button label="Photo" />
        <el-radio-button label="Request" />
        <el-radio-button label="Setting" />
      </el-radio-group>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const radio1 = ref('New York')
const radio2 = ref('New York')
const radio3 = ref('New York')
const mode = ref('Main')
</script>
