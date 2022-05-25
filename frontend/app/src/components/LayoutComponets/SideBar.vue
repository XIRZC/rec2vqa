<template>
  <el-row class="tac">
    <el-col>
      <el-menu
        :default-active="mode_idx"
        class="el-menu-vertical-demo"
        @select="set_mode"
      >
        <el-menu-item index="1">
          <el-icon><icon-menu /></el-icon>
          <span>{{main_text}}</span>
        </el-menu-item>
        <el-menu-item index="2">
          <el-icon><picture-filled /></el-icon>
          <span>{{photo_text}}</span>
        </el-menu-item>
        <el-menu-item index="3">
          <el-icon><clock /></el-icon>
          <span>{{history_text}}</span>
        </el-menu-item>
        <el-menu-item index="4">
          <el-icon><setting /></el-icon>
          <span>{{setting_text}}</span>
        </el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { useStore } from '../../store'
import { computed, ref } from 'vue'
import {
  Menu as IconMenu,
  Setting,
  PictureFilled,
  Clock,
} from '@element-plus/icons-vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const store = useStore()
const main_text = computed( () => store.state.locale[store.state.locale.lang].SideBar.main)
const photo_text = computed( () => store.state.locale[store.state.locale.lang].SideBar.photo)
const history_text = computed( () => store.state.locale[store.state.locale.lang].SideBar.history)
const setting_text = computed( () => store.state.locale[store.state.locale.lang].SideBar.setting)
const idx2mode = {
  "1": "Main",
  "2": "Photo",
  "3": "Request",
  "4": "Setting",
}
const mode2idx = {
  "Main": "1",
  "Photo": "2",
  "Request": "3",
  "Setting": "4",
}
const mode = computed( () => store.state.mode )
const mode_idx = computed( () => mode2idx[mode.value] )
console.log('mode_idx', mode_idx)


// const mode = computed(() => store.state.mode)
const set_mode = (key, keyPath) => {
  router.push({ name: 'app', params: { mode: idx2mode[key] }})
}
</script>
