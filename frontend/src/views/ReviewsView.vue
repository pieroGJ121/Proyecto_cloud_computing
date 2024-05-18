<template>
  <LayoutComponent>
    <template #Content>
      <h2 class="titulo-market">
        Desde aquí podras administrar todas las reseñas que has publicado hasta
        ahora
      </h2>
      <div class="container-market">
        <div class="row-market" v-for="review in reviews" :key="review.id">
          <div class="column-market-image">
            <div class="image-container-market">
              <img :src="review.game.cover" alt="Image" />
            </div>
          </div>
          <div class="column-market-content">
            <h2 class="nombre">Nombre del juego: {{ review.game.name }}</h2>
            <div class="form_group_game_market">
              <label for="title" class="label-market">Título de reseña</label>
              <div class="custom-select-market">
                <input
                  type="text"
                  id="title"
                  class="form_control_game_market"
                  :value="review.title"
                  required
                  disabled
                />
              </div>
            </div>
            <div class="form_group_game_market">
              <label for="platform" class="label-market">Plataforma</label>
              <div class="custom-select-market">
                <input
                  type="text"
                  id="platform"
                  class="form_control_game_market"
                  :value="review.platform"
                  required
                  disabled
                />
              </div>
            </div>
            <div class="form_group_game_market">
              <label for="comment" class="label-market">Comentario</label>
              <div class="custom-select-market">
                <input
                  type="text"
                  id="comment"
                  class="form_control_game_market"
                  :value="review.comment"
                  required
                  disabled
                />
              </div>
            </div>
            <div class="botones-market">
              <button
                class="actualizar-market"
                @click="updateReview(review.id)"
              >
                Actualizar
              </button>
              <button class="eliminar-market" @click="deleteReview(review.id)">
                Eliminar
              </button>
            </div>
          </div>
        </div>

        <h1 v-if="showMessage">
          Aún no has publicado tu reseña de ningún juego.
        </h1>
      </div>
    </template>
  </LayoutComponent>
</template>

<script>
import LayoutComponent from "@/components/Layout.vue";
import { verifier_login } from "@/services/login.api";
import {
  getReviews,
  confirmDeletionReview,
  deleteReview,
} from "@/services/review.api";

export default {
  name: "ReviewsView",
  components: {
    LayoutComponent,
  },
  data() {
    return {
      reviews: [],
      showMessage: false,
    };
  },
  async mounted() {
    await verifier_login();
    const data = await getReviews();
    this.reviews = data.reviews;
    if (this.reviews.length === 0) {
      this.showMessage = true;
    }
  },
  methods: {
    async deleteReview(id) {
      const result = await confirmDeletionReview();
      if (result.isConfirmed) {
        try {
          await deleteReview(id);
          const data = await getReviews();
          this.reviews = data.reviews;
        } catch (error) {
          console.log(error);
        }
      }
    },
    updateReview(id) {
      window.location.href = `/change_review?id=${id}`;
    },
  },
};
</script>

<style>
@import url("../css/marketplace/update_game.css");
</style>
