<template>
    <el-container direction="horizontal">
      <el-container style="padding: 10px 70px">
        <el-container direction="vertical" style="max-width: 400px; text-align: center">
        <el-breadcrumb :separator-icon="ArrowRight" style="margin-bottom: 10px">
          <el-breadcrumb-item :to="{ name: 'app', params: { mode: 'Request' }}">REC List</el-breadcrumb-item>
          <el-breadcrumb-item >REC Detail</el-breadcrumb-item>
        </el-breadcrumb>
          <div class="demo-image">
            <div class="block">
              <el-image :src="request.result_image" fit="cover" />
            </div>
          </div>
        </el-container>
        <el-container direction="vertical" style="max-width: 500px; padding: 5px 30px; height: 420px">
          <el-scrollbar>
            <div style="margin: 20px" />
            <el-form
              label-position="top"
              label-width="100px"
              style="max-width: 400px"
            >
            <div style="font-size: 15px; font-weight: bold">
              Step 1: Referring Expression Comprehension (REC)
            </div>
              <el-form-item label="Referring Expression:">
                <el-contianer direction="horizontal" style="width: 400px">
                  <el-input v-model="request.parent_referring_expression" disabled />
                </el-contianer>
              </el-form-item>
              <el-form-item label="Detection Results:">
                <el-input v-model="request.parent_result" disabled />
              </el-form-item>
            </el-form>
            <el-form
              v-if="request.vqas == undefined"
              label-position="top"
              label-width="100px"
              style="max-width: 400px"
            >
              <div style="font-size: 15px; font-weight: bold">
                Step 2: Visual Question Answering (VQA)
              </div>
              <el-form-item label="Question:">
                <el-contianer direction="horizontal" style="width: 400px">
                  <el-input v-model="request.referring_expression" disabled />
                </el-contianer>
              </el-form-item>
              <el-form-item label="Answer:">
                <el-input v-model="request.result" disabled />
              </el-form-item>
            </el-form>
            <VqaForm v-else/>
          </el-scrollbar>
        </el-container>
      </el-container>
    </el-container>
</template>

<script lang="ts" setup>
import { useStore } from "../../store";
import { computed } from "vue";
import VqaForm from "../ContentComponents/VqaForm.vue";
import { ArrowRight } from '@element-plus/icons-vue'

const store = useStore()
const mode = computed(() => store.state.mode)
const has_rec_posted = computed(() => store.state.has_rec_posted)
const request = computed( () => store.state.last_rec_post)
// console.log('last_rec_post', request)
</script>


<style scoped>
.demo-image .block {
  padding: 10px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 100%;
  box-sizing: border-box;
  vertical-align: top;
}
.demo-image .block:last-child {
  border-right: none;
}
.demo-image .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>
