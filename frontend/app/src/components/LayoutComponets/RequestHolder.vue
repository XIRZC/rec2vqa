<template>
    <el-container direction="horizontal">
      <el-container style="padding: 10px 70px">
        <el-container direction="vertical" style="max-width: 400px; text-align: center">
        <el-breadcrumb :separator-icon="ArrowRight" style="margin-bottom: 10px">
          <el-breadcrumb-item :to="{ name: 'app', params: { mode: 'Request' }}">{{rec_list_text}}</el-breadcrumb-item>
          <el-breadcrumb-item >{{rec_detail_text}}</el-breadcrumb-item>
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
              {{rec_title_text}}
            </div>
              <el-form-item :label="rec_exp_text">
                <el-contianer direction="horizontal" style="width: 400px">
                  <el-input v-model="request.parent_referring_expression" disabled />
                </el-contianer>
              </el-form-item>
              <el-form-item :label="rec_res_text">
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
                {{vqa_title_text}}
              </div>
              <el-form-item :label="vqa_question_text">
                <el-contianer direction="horizontal" style="width: 400px">
                  <el-input v-model="request.referring_expression" disabled />
                </el-contianer>
              </el-form-item>
              <el-form-item :label="vqa_answer_text">
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

const rec_list_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.rec_list )
const rec_detail_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.rec_detail )
const table_id_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_id )
const table_re_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_re )
const table_res_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_res )
const table_image_url_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_image_url )
const table_image_link_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_image_link )
const table_vqa_entry_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_vqa_entry )
const table_vqa_detail_text = computed( () => store.state.locale[store.state.locale.lang].RequestHistory.table_vqa_detail )

const rec_title_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.title)
const rec_exp_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.exp)
const rec_placeholder_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.placeholder)
const rec_submit_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.submit)
const rec_res_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.res)
const rec_dialog_ensure_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.dialog_ensure)
const rec_dialog_confirm_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.dialog_confirm)
const rec_dialog_cancel_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.dialog_cancel)

const vqa_title_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.title)
const vqa_question_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.question)
const vqa_placeholder_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.placeholder)
const vqa_submit_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.submit)
const vqa_answer_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.answer)
const vqa_dialog_ensure_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.dialog_ensure)
const vqa_dialog_confirm_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.dialog_confirm)
const vqa_dialog_cancel_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.dialog_cancel)

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
