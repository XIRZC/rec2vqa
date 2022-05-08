<template>
  <div class="switcher">
    <el-button-group>
      <el-button @click="previousSlide" type="primary" :icon="ArrowLeft">Previous Slide</el-button>
      <el-button @click="nextSlide" type="primary">
        Next Slide<el-icon class="el-icon--right"><ArrowRight /></el-icon>
      </el-button>
    </el-button-group>
  </div>
</template>

<script setup lang="ts">
import { useStore } from '../../store'
import {
  ArrowLeft,
  ArrowRight,
} from '@element-plus/icons-vue';
const store = useStore()
store.commit('set_show_img', {
    mode: 'list',
});
const previousSlide = () => {
    store.commit('set_show_img', {
        mode: 'previous',
    });
    store.commit('set_has_rec_posted', {
      bin: false,
    });
};
const nextSlide = () => {
    store.commit('set_show_img', {
        mode: 'next',
    });
    store.commit('set_has_rec_posted', {
      bin: false,
    });
};
</script>

<style scoped>
.switcher {
  padding: 10px 0;
  text-align: center;
  display: inline-block;
  width: 100%;
  box-sizing: border-box;
  vertical-align: top;
}
</style>