<template>
  <div style="margin: 20px" />
  <el-form
    label-position="top"
    label-width="100px"
    :model="formData"
    style="max-width: 800px"
  >
  <div style="font-size: 15px; font-weight: bold">
    {{title_text}}
  </div>
    <el-form-item :label="exp_text">
      <el-contianer direction="horizontal" style="width: 800px">
        <el-input v-model="formData.referring_expression"
         style="max-width: 640px"
         type="textarea"
         autosize
         clearable
         maxlength="80"
         show-word-limit
         :placeholder="placeholder_text"  />
        <el-button type="primary" @click="rec_dialog_show = true" style="margin-left: 5px"
          >{{submit_text}}</el-button
        >
      </el-contianer>
    </el-form-item>
    <el-form-item :label="res_text">
      <el-input v-model="formData.res" disabled />
    </el-form-item>
  </el-form>
  <el-dialog v-model="rec_dialog_show" width="30%" center draggable>
    <span
      >{{dialog_ensure_text}}
      </span
    >
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="rec_dialog_show = false">{{dialog_cancel_text}}</el-button>
        <el-button type="primary" @click="onSubmit"
          >{{dialog_confirm_text}}</el-button
        >
      </span>
    </template>
  </el-dialog>
</template>


<script lang="ts" setup>
import { useStore } from "../../store";
import { computed } from "vue";
import { reactive, ref } from 'vue'
import { useWebSocket } from "../../hooks";
import { v4 as uuidv4} from 'uuid';
import { ElLoading } from 'element-plus'

const store = useStore()
const URL = computed(() => store.state.URL_PREFIX)
const has_rec_posted = computed(() => store.state.has_rec_posted)
const show_img_id = computed(() => store.state.show_img.id)

const title_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.title)
const exp_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.exp)
const placeholder_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.placeholder)
const submit_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.submit)
const res_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.res)
const dialog_ensure_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.dialog_ensure)
const dialog_confirm_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.dialog_confirm)
const dialog_cancel_text = computed( () => store.state.locale[store.state.locale.lang].RecForm.dialog_cancel)

const axios = require('axios');
const rec_dialog_show = ref(false)

// const ws = useWebSocket(handleOpen, handleMessage);
// function handleOpen (e) {
//   console.log("User connected to the socket with socketid "+ socket_id);
//   ws.send(JSON.stringify({
//     socket_id: socket_id,
//   }));
// };
// function handleMessage (response) {
//   console.log("Getting response from the worker.....");
//   console.log(JSON.parse(response.data));

//   response = JSON.parse(response.data);

//   if ("info" in response){
//     console.log("Info is there as the key");
//   }

//   if ("result" in response){
//     console.log('result come up')
//   }
// };

// do not use same name with ref
const formData = reactive({
  referring_expression: '',
  res: '',
  img: 0,
  socket_id: ''
})

const onSubmit = () => {
  rec_dialog_show.value = false
  const socket_id = uuidv4()
  console.log('socket_id', socket_id)
  formData.img = show_img_id.value
  formData.socket_id = socket_id
  console.log('rec submit!', formData)
  axios.post(URL.value + 'recs/', formData)
    .then( (response) => {
      console.log('rec post response data:', response, response.data);
      store.commit('set_last_rec_post', response.data)
      const query_socket_id = response.data.socket_id
      const loadingInstance = ElLoading.service({
        lock: true,
        text: 'Loading...',
        background: 'rgba(0, 0, 0, 0.7)',
      })
      setTimeout(() => {
        console.log('------', URL.value + 'socket' + query_socket_id)
        axios.get(URL.value + 'socket', {
          params: {
            socket_id: query_socket_id,
            task: 'rec',
          }
        })
          .then( (response)  => {
            var data = response.data[0]
            const pk = data.pk
            const fields = data.fields
            fields.id = pk
            console.log('get rec id data:', fields)
            store.commit('set_last_rec_post', fields)
            formData.res = fields.result
            console.log(formData.res)
            store.commit('set_show_img', {
              mode: 'show',
              img: fields.result_image,
            })
          })
        loadingInstance.close()
      }, 1000)
    })
    .catch( (error) => {
      console.log(error);
    })
    .then( () => {
    })
  store.commit('set_has_rec_posted', {
    bin: true,
  });
}
</script>

<style scoped>
.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>
