import { createStore, useStore as baseUseStore, Store } from 'vuex'
import { InjectionKey } from 'vue'

// define your typings for the store state
// locale for switch between english and chinese, key by lang, value split by component
export interface HeaderBar {
  header_text: string,
  home_site_name: string,
  about_site_name: string,
  app_site_name: string
}
export interface SideBar {
  main: string,
  photo: string,
  history: string,
  setting: string,
}
export interface MainHolder {
  select: string,
  upload: string,
}
export interface SwitchHolder {
  previous: string,
  next: string,
}
export interface UploadHolder {
  select: string,
  upload: string,
}
export interface RecForm {
  title: string,
  exp: string,
  placeholder: string,
  submit: string,
  res: string,
  dialog_ensure: string,
  dialog_confirm: string,
  dialog_cancel: string,
}
export interface VqaForm {
  title: string,
  question: string,
  placeholder: string,
  submit: string,
  answer: string,
  dialog_ensure: string,
  dialog_confirm: string,
  dialog_cancel: string,
}
export interface RequestHistory {
  rec_list: string,
  rec_detail: string,
  table_id: string,
  table_re: string,
  table_res: string,
  table_image_url: string,
  table_image_link: string,
  table_vqa_entry: string,
  table_vqa_detail: string,
}
export interface SettingPanel {
  lang: string,
  shuffle: string,
  shuffle_yes: string,
  shuffle_no: string,
}
export interface Components {
  HeaderBar: HeaderBar,
  SideBar: SideBar,
  MainHolder: MainHolder,
  SwitchHolder: SwitchHolder,
  UploadHolder: UploadHolder,
  RecForm: RecForm,
  VqaForm: VqaForm,
  RequestHistory: RequestHistory,
  SettingPanel: SettingPanel,
}
export interface Locale {
  en: Components,
  cn: Components,
  lang: string,
}
export interface Image {
  id: number,
  img: string,
}
export interface ShowImage {
  url: string,
  idx: number,
  list: Array<Image>,
  id: number
}

export interface VQA {
  id: number,
  question: string,
  answer: string,
  rec: number,
  parent_referring_expression: string,
  parent_result: string,
}

export interface REC {
  id: number,
  img: number,
  image: string,
  referring_expression: string,
  result: string,
  parent_referring_expression: string,
  parent_result: string,
  result_image: string,
  vqas: VQA[];
  chidren: VQA[];
}

export interface State {
  shuffule_img_list: boolean,
  locale: Locale,
  URL_PREFIX: string,
  mode: string,
  has_rec_posted: boolean,
  show_img: ShowImage,
  last_rec_post: REC,
  recs: REC[];
}

// define injection key
export const key: InjectionKey<Store<State>> = Symbol()

export const store = createStore<State>({
  state: {
    shuffule_img_list: false,
    locale: {
      lang: 'cn',
      en: {
        HeaderBar: {
          header_text: 'Referring Expression Comprehension Based Visual Question Answering',
          home_site_name: 'Home',
          about_site_name: 'About',
          app_site_name: 'App',
        },
        SideBar: {
          main: 'Main Operator',
          photo: 'Photo Wall',
          history: 'Request History',
          setting: 'Setting',
        },
        MainHolder: {
          select: 'Select From PhotoWall',
          upload: 'Upload Only One Photo',
        },
        SwitchHolder: {
          previous: 'Previous Slide',
          next: 'Next Slide',
        },
        UploadHolder: {
          select: 'Select File',
          upload: 'Upload To Server',
        },
        RecForm: {
          title: 'Step 1: Referring Expression Comprehension (REC)',
          exp: 'Referring Expression:',
          placeholder: 'Please input a referring expression : )',
          submit: 'Submit',
          res: 'Detection Results:',
          dialog_ensure: 'Confirm to submit rec form data?',
          dialog_confirm: 'Confirm',
          dialog_cancel: 'Cancel',
        },
        VqaForm: {
          title: 'Step 2: Visual Question Answering (VQA)',
          question: 'Question:',
          placeholder: 'Please input a question : )',
          submit: 'Submit',
          answer: 'Answer:',
          dialog_ensure: 'Confirm to submit vqa form data?',
          dialog_confirm: 'Confirm',
          dialog_cancel: 'Cancel',
        },
        RequestHistory: {
          rec_list: 'REC List',
          rec_detail: 'REC Detail',
          table_id: 'ID',
          table_re: 'Referring Expression',
          table_res: 'Detection Result',
          table_image_url: 'Image URL',
          table_image_link: 'Image Link',
          table_vqa_entry: 'VQA Entry',
          table_vqa_detail: 'VQA Detail',
        },
        SettingPanel: {
          lang: 'Language Setting: ',
          shuffle: 'Shuffle Image List Setting: ',
	  shuffle_yes: 'Yes',
	  shuffle_no: 'No',
        },
      },
      cn: {
        HeaderBar: {
          header_text: '基于指称表达式所指代物体的视觉问题回答',
          home_site_name: '主页',
          about_site_name: '关于',
          app_site_name: '应用',
        },
        SideBar: {
          main: '操作界面',
          photo: '图片墙',
          history: '请求历史',
          setting: '设置',
        },
        MainHolder: {
          select: '从图片墙中选择',
          upload: '仅上传一张图片',
        },
        SwitchHolder: {
          previous: '上一张',
          next: '下一张',
        },
        UploadHolder: {
          select: '选择文件',
          upload: '上传至服务器',
        },
        RecForm: {
          title: '步骤一：指称表达式理解',
          exp: '指称表达式：',
          placeholder: '请输入一个指称表达式',
          submit: '提交',
          res: '检测结果：',
          dialog_ensure: '确认提交指称表达式理解的表达数据吗？',
          dialog_confirm: '确认',
          dialog_cancel: '取消',
        },
        VqaForm: {
          title: '步骤二：视觉问题回答',
          question: '问题：',
          placeholder: '请输入一个问题',
          submit: '提交',
          answer: '答案：',
          dialog_ensure: '确认提交视觉问题回答的表达数据吗？',
          dialog_confirm: '确认',
          dialog_cancel: '取消',
        },
        RequestHistory: {
          rec_list: '指称表达理解列表',
          rec_detail: '指称表达理解详情',
          table_id: '编号',
          table_re: '指称表达式',
          table_res: '检测结果',
          table_image_url: '图片链接',
          table_image_link: '图片链接',
          table_vqa_entry: '视觉问答详情',
          table_vqa_detail: '视觉问答详情',
        },
        SettingPanel: {
          lang: '语言设置：',
          shuffle: '图片列表乱序设置：',
	  shuffle_yes: '是',
	  shuffle_no: '否',
        },
      }
    },
    URL_PREFIX : "http://region-7.autodl.com:28417/",
    // URL_PREFIX: 'http://region-11.autodl.com:13142/';
    mode: "Main",  // SideBar menubar set mode, and MainHolder get mode
    has_rec_posted: false,  // MainHolder controller for show vqafrom comp
    show_img: {
      url: '',
      idx: 1,
      list: [],
      id: 1,
    },
    last_rec_post: {
      id: 1,
      img: 1,
      image: '',
      referring_expression: '',
      result: '',
      parent_referring_expression: '',
      parent_result: '',
      result_image: '',
      vqas: [],
      chidren: [],
    },
    recs: [],
  },
  getters: {
  },
  mutations: {
    set_mode (state, payload) {
      const idx2mode = {
        "1": "Main",
        "2": "Photo",
        "3": "Request",
        "4": "Setting",
      }
      state.mode = idx2mode[payload.index];
      // console.log('store mode', state.mode)
    },
    set_has_rec_posted (state, payload) {
      state.has_rec_posted = payload.bin;
      // console.log('has_rec_posted', state.has_rec_posted)
    },
    set_show_img (state, payload) {
      if ( payload.mode === 'next') {
        if ( state.show_img.idx < state.show_img.list.length ) {
          state.show_img.idx ++;
        }
      }
      else if ( payload.mode === 'list' ) {
        state.show_img.list = payload.list;
        // console.log('show_img_list', state.show_img.list)
      }
      else if ( payload.mode === 'upload' ) {  // upload
        state.show_img.url = payload.data.img
        state.show_img.id = payload.data.id
      }
      else if ( payload.mode === 'show' ) {  // show
        state.show_img.url = payload.img
        console.log('payload.img', payload.img)
      }
      else {  // previous
        if ( state.show_img.idx > 1 ) {
          state.show_img.idx --;
        }
      }
      if (state.show_img.list != undefined && payload.mode != 'upload' && payload.mode != 'show') {
        state.show_img.url = state.show_img.list[state.show_img.idx-1].img
        state.show_img.id = state.show_img.list[state.show_img.idx-1].id
      }
      // console.log(state.show_img)
    },
    set_last_rec_post (state, payload) {
      state.last_rec_post = payload
      console.log('last_rec_post', state.last_rec_post)
    },
    set_recs (state, payload) {
      store.state.recs = payload
      console.log('recs', store.state.recs)
    },
    set_locale_lang (state, payload) {
      console.log('set locale lang', payload)
      store.state.locale.lang = payload
    },
    set_shuffle_img_list (state, payload) {
      console.log('set shuffle img list', payload)
      store.state.shuffule_img_list = payload
      console.log('setted shuffle img list', store.state.shuffule_img_list)
    },
  },
  actions: {
  },
  modules: {
  }
})

// define your own `useStore` composition function
export function useStore () {
  return baseUseStore(key)
}
