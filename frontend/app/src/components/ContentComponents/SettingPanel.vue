<template>
    <el-form>
        <el-form-item :label="lang_text">
            <el-switch
              v-model="lang"
              class="mb-2"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-text="中文"
              inactive-text="English"
              active-value="cn"
              inactive-value="en"
              @change="onLangChange"
            />
        </el-form-item>
        <el-form-item :label="shuffle_text">
            <el-switch
              v-model="shuffle_img_list"
              class="mb-2"
              active-color="#13ce66"
              inactive-color="#ff4949"
              :active-text="shuffle_yes_text"
              :inactive-text="shuffle_no_text"
              @change="onShuffleChange"
            />
        </el-form-item>
    </el-form>
</template>
<script lang="ts" setup>
import { computed } from 'vue';
import { ref } from 'vue'
import { useStore } from "../../store";

const store = useStore()
const lang = computed( () => store.state.locale.lang )
const shuffle_img_list = computed ( () => store.state.shuffule_img_list)
const lang_text = computed( () => store.state.locale[store.state.locale.lang].SettingPanel.lang)
const shuffle_text = computed( () => store.state.locale[store.state.locale.lang].SettingPanel.shuffle)
const shuffle_yes_text = computed( () => store.state.locale[store.state.locale.lang].SettingPanel.shuffle_yes)
const shuffle_no_text = computed( () => store.state.locale[store.state.locale.lang].SettingPanel.shuffle_no)

const onLangChange = function (val) {
    console.log('global lang', val)
    store.commit('set_locale_lang', val)
}
const onShuffleChange = function (val) {
    console.log('global shuffle', val)
    store.commit('set_shuffle_img_list', val)
}
</script>
