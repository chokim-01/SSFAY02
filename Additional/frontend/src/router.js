import Vue from "vue"
import Router from "vue-router"
import NewsList from "./views/NewsList.vue"
import AboutUs from "./views/AboutUs.vue"
import NewsDetail from "./components/NewsDetail.vue"

Vue.use(Router)


export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [{
      path: "/",
      name: "NewsList",
      component: NewsList
    },
    {
        path: "/AboutUs",
        name: "AboutUs",
        component: AboutUs
    },
    {
        path: "/NewsDetail",
        name: "NewsDetail",
        component: NewsDetail
    }
  ]
})
