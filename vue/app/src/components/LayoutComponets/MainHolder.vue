<template>
    <el-container direction="horizontal">
      <el-container style="padding: 10px 70px" v-if="props.app === 'Main'">
        <el-container direction="vertical" style="max-width: 900px; text-align: center">
          <div>
            <el-radio-group v-model="choice_radio">
              <el-radio-button label="Select From PhotoWall">{{select_text}}</el-radio-button>
              <el-radio-button label="Upload Only One Photo">{{upload_text}}</el-radio-button>
            </el-radio-group>
          </div>
          <SwitchHolder v-if="choice_radio === 'Select From PhotoWall'" />
          <UploadHolder v-else />
          <ImageHolder />
        </el-container>
        <el-container direction="vertical" style="max-width: 800px; padding: 5px 30px; height: 800px; margin-top: 70px;">
          <el-scrollbar>
            <RecForm />
            <VqaForm v-if="has_rec_posted"/>
          </el-scrollbar>
        </el-container>
      </el-container>
      <el-container style="padding: 10px 50px" v-else-if="props.app === 'Photo'">
        <PhotoWall />
      </el-container>
      <el-container style="padding: 10px 20px" v-else-if="props.app === 'Request'">
        <RequestHistory />
      </el-container>
      <el-container style="padding: 10px 50px" v-else-if="props.app === 'Setting'">
        <SettingPanel />
      </el-container>
    </el-container>
</template>

<script lang="ts" setup>
import { useStore } from "../../store";
import { computed } from "vue";
import ImageHolder from "../ContentComponents/ImageHolder.vue";
import UploadHolder from "../ContentComponents/UploadHolder.vue";
import SwitchHolder from "../ContentComponents/SwitchHolder.vue";
import RecForm from "../ContentComponents/RecForm.vue";
import VqaForm from "../ContentComponents/VqaForm.vue";
import PhotoWall from "../ContentComponents/PhotoWall.vue";
import RequestHistory from "../ContentComponents/RequestHistory.vue";
import SettingPanel from "../ContentComponents/SettingPanel.vue";
import { ref } from 'vue'

const props = defineProps(['app'])
console.log('props.app', props.app)

const choice_radio = ref('Select From PhotoWall')
const store = useStore()
const mode = computed(() => store.state.mode)
const select_text = computed(() => store.state.locale[store.state.locale.lang].MainHolder.select)
const upload_text = computed(() => store.state.locale[store.state.locale.lang].MainHolder.upload)
const has_rec_posted = computed(() => store.state.has_rec_posted)
</script>