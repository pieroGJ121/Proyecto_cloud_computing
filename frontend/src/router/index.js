import { createRouter, createWebHistory } from "vue-router";
import IndexView from "../views/IndexView.vue";
import LoginView from "../views/LoginView.vue";
import NewUserView from "../views/NewUserView.vue";
import RecoverUserView from "../views/RecoverUserView.vue";
import ProfileView from "../views/ProfileView.vue";
import SearchView from "../views/SearchView.vue";
import VideogameView from "../views/VideogameView.vue";
import ReviewsView from "../views/ReviewsView.vue";
import RatingsView from "../views/RatingsView.vue";
import PostReviewView from "../views/PostReviewView.vue";
import PostRatingView from "../views/PostRatingView.vue";
import UpdateReviewView from "../views/UpdateReviewView.vue";
import UpdateRatingView from "../views/UpdateRatingView.vue";

const routes = [
  {
    path: "/",
    name: "index",
    meta: { title: "Mira las opiniones de los mejores juegos" },
    component: IndexView,
  },
  {
    path: "/login",
    name: "login",
    meta: { title: "Inicia aquí y ahora" },
    component: LoginView,
  },
  {
    path: "/new_user",
    name: "new_user",
    meta: { title: "Unete a esta gran experiencia" },
    component: NewUserView,
  },
  {
    path: "/password_recovery",
    name: "password_recovery",
    meta: { title: "Recupere su contraseña" },
    component: RecoverUserView,
  },
  {
    path: "/profile",
    name: "profile",
    meta: { title: "Perfil del usuario" },
    component: ProfileView,
  },
  {
    path: "/search",
    name: "search",
    meta: { title: "Resultados de la busqueda" },
    component: SearchView,
  },
  {
    path: "/videogame",
    name: "videogame",
    meta: { title: "Detalles del videojuego" },
    component: VideogameView,
  },
  {
    path: "/ratings",
    name: "ratings",
    meta: { title: "Centro de ratings del usuario" },
    component: RatingsView,
  },
  {
    path: "/reviews",
    name: "reviews",
    meta: { title: "Centro de reviews del usuario" },
    component: ReviewsView,
  },
  {
    path: "/new_rating",
    name: "new_rating",
    meta: { title: "Publica tu rating" },
    component: PostRatingView,
  },
  {
    path: "/new_review",
    name: "new_review",
    meta: { title: "Publica tu review" },
    component: PostReviewView,
  },
  {
    path: "/change_rating",
    name: "change_rating",
    meta: { title: "Actualiza tu rating" },
    component: UpdateRatingView,
  },
  {
    path: "/change_review",
    name: "change_review",
    meta: { title: "Actualiza tu review" },
    component: UpdateReviewView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title;
  next();
});

export default router;
