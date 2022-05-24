import { createApp } from "vue";
import App from "./App.vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import router from "./router";
import { store, key } from './store'

createApp(App).use(ElementPlus).use(store, key).use(router).mount("#app");
