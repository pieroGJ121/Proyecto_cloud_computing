<template>
  <LayoutComponent>
    <template #Content>
      <h2 class="titulo-market">
        Desde aquí podras administrar todos los puntajes que has publicado hasta
        ahora
      </h2>
      <div class="container-market">
        <div class="row-market" v-for="rating in ratings" :key="rating.id">
          <div class="column-market-image">
            <div class="image-container-market">
              <img :src="rating.game.cover" alt="Image" />
            </div>
          </div>
          <div class="column-market-content">
            <h2 class="nombre">Nombre del juego: {{ rating.game.name }}</h2>
            <div class="form_group_game_market">
              <label for="score" class="label-market">Puntaje</label>
              <input
                type="number"
                id="score"
                class="form_control_game_market"
                :value="rating.score"
                required
                disabled
              />
            </div>
            <div class="botones-market">
              <button
                class="actualizar-market"
                @click="updateRating(rating.id)"
              >
                Actualizar
              </button>
              <button class="eliminar-market" @click="deleteRating(rating.id)">
                Eliminar
              </button>
            </div>
          </div>
        </div>

        <h1 v-if="showMessage">
          Aún no has publicado tu puntaje de ningún juego.
        </h1>
      </div>
    </template>
  </LayoutComponent>
</template>

<script>
import LayoutComponent from "@/components/Layout.vue";
import { verifier_login } from "@/services/login.api";
import {
  getRatings,
  confirmateDeletionRating,
  deleteRating,
} from "@/services/rating.api";

export default {
  name: "RatingsView",
  components: {
    LayoutComponent,
  },
  data() {
    return {
      ratings: [],
      showMessage: false,
    };
  },
  async mounted() {
    await verifier_login();
    const data = await getRatings();
    this.ratings = data.ratings;
    if (this.ratings.length === 0) {
      this.showMessage = true;
    }
  },
  methods: {
    async deleteRating(id) {
      const result = await confirmateDeletionRating();
      if (result.isConfirmed) {
        try {
          await deleteRating(id);
          const data = await getRatings();
          this.ratings = data.rating;
        } catch (error) {
          console.log(error);
        }
      }
    },
    updateRating(id) {
      window.location.href = `/change_rating?id=${id}`;
    },
  },
};
</script>

<style>
@import url("../css/marketplace/update_game.css");
</style>
