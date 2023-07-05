<template>
  <LayoutComponent>
    <template #Content>
      <h2 class="search_text_p" id="welcome_text">
        {{ user_name }}, estos son los juegos que has comprado:
      </h2>
      <div class="main_container_games">
        <div class="container_games" id="container_games">
          <div
            class="item_game"
            v-for="juego in games"
            :key="juego.game.api_id"
            @click="getVideogame(juego.game.api_id)"
          >
            <img :src="juego.game.cover" :alt="juego.game.name" />
            <h4 style="color: white">{{ juego.game.name }}</h4>
            <p>Publicado en: {{ juego.game.release_year }}</p>
          </div>
        </div>
      </div>
      <h3 class="search_results_counter" id="counter_games">
        En total has adquirido {{ games.length }} juegos
      </h3>
    </template>
  </LayoutComponent>
</template>

<script>
import LayoutComponent from "@/components/Layout.vue";
//import { verifier_login } from "@/services/login.api";

export default {
  name: "PurchasesView",
  components: {
    LayoutComponent,
  },
  data() {
    return {
      games: [],
      user_name: "",
    };
  },
  async mounted() {
    //verifier_login();
  },
};
</script>

<style>
@import url("../css/purchases/purchases.css");
</style>
