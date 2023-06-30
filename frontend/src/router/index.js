import { createRouter, createWebHistory } from "vue-router";
import IndexView from "../views/IndexView.vue";
import LoginView from "../views/LoginView.vue";
import LogoutView from "../views/LogoutView.vue";
import NewUserView from "../views/NewUserView.vue";

const routes = [
  {
    path: "/",
    name: "index",
    meta: { title: "Compra los mejores juegos aquí" },
    component: IndexView,
  },
  {
    path: "/login",
    name: "login",
    meta: { title: "Inicia aquí y ahora" },
    component: LoginView,
  },
  {
    path: "/logout",
    name: "logout",
    meta: { title: "Esperamos verte pronto :)" },
    component: LogoutView,
  },
  {
    path: "/new_user",
    name: "new_user",
    meta: { title: "Unete a esta gran experiencia" },
    component: NewUserView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  console.log(to);
  document.title = to.meta.title;
  next();
});

export default router;
