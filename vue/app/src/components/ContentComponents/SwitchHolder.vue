<template>
  <div class="switcher">
    <el-button-group>
      <el-button @click="previousSlide" type="primary" :icon="ArrowLeft">{{previous_text}}</el-button>
      <el-button @click="nextSlide" type="primary">
        {{next_text}}<el-icon class="el-icon--right"><ArrowRight /></el-icon>
      </el-button>
    </el-button-group>
  </div>
</template>

<script setup lang="ts">
import { useStore } from '../../store'
import { computed } from 'vue'
import {
  ArrowLeft,
  ArrowRight,
} from '@element-plus/icons-vue';
const store = useStore()
const previous_text = computed( () => store.state.locale[store.state.locale.lang].SwitchHolder.previous )
const next_text = computed( () => store.state.locale[store.state.locale.lang].SwitchHolder.next )
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