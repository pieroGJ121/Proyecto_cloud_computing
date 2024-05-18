<template>
  <LayoutComponent>
    <template #Content>
      <div class="container_form_game_sell">
        <h1>Actualiza tu oferta en pocco tiempo 😁</h1>
        <form
          id="game_form_game_sell"
          class="game_form_game_sell"
          @submit.prevent.stop="updateOffer()"
        >
          <div class="columna-sell">
            <div class="form_group_game_sell">
              <label for="name" class="label-sell">NOMBRE DEL JUEGO</label>
              <input
                type="text"
                id="name_sell"
                class="form_control_game_sell"
                :value="game.name ? game.name : 'Getting data'"
                required
                disabled
              />
            </div>
            <div class="form_group_game_sell">
              <label for="genre" class="label-sell">GÉNERO</label>
              <input
                type="text"
                id="name_sell"
                class="form_control_game_sell"
                :value="game.genres ? game.genres.join(', ') : 'Getting data'"
                required
                disabled
              />
            </div>
            <div class="form_group_game_sell">
              <label for="platforms" class="label-sell">PLATAFORMAS</label>
              <div class="custom-select-sell">
                <select
                  id="platforms_review"
                  class="form_control_game_sell"
                  v-model="platform_selected"
                  required
                  :disabled="platforms.length === 0"
                >
                  <option v-for="(platform, index) in platforms" :key="index">
                    {{ platform }}
                  </option>
                </select>
              </div>
            </div>
            <div class="form_group_game_sell">
              <label for="title" class="label-sell">TÏTULO DE LA REVIEW</label>
              <div class="custom-select-sell">
                <input
                  type="text"
                  id="title"
                  class="form_control_game_sell"
                  v-model="title"
                  required
                />
              </div>
            </div>
            <div class="form_group_game_sell">
              <label for="comment" class="label-sell">COMENTARIO</label>
              <div class="custom-select-sell">
                <input
                  type="text"
                  id="comment"
                  class="form_control_game_sell"
                  v-model="comment"
                  required
                />
              </div>
            </div>
          </div>
          <div class="columna-sell">
            <div class="form_group_game_sell">
              <label for="release_date" class="label-sell"
                >FECHA DE LANZAMIENTO</label
              >
              <input
                type="text"
                id="name_sell"
                class="form_control_game_sell"
                :value="game.release_year ? game.release_year : 'Getting data'"
                required
                disabled
              />
            </div>
            <div class="form_group_game_sell">
              <label for="publisher" class="label-sell">EDITOR</label>
              <div class="custom-select-sell">
                <input
                  type="text"
                  id="name_sell"
                  class="form_control_game_sell"
                  :value="
                    game.involved_companies
                      ? game.involved_companies.join(', ')
                      : 'Getting data'
                  "
                  required
                  disabled
                />
              </div>
            </div>
            <div class="form_group_game_sell">
              <label for="synopsis" class="label-sell">SINOPSIS</label>
              <textarea
                id="synopsis_sell"
                class="form_control_game_sell"
                :value="game.summary ? game.summary : 'Getting data'"
                required
                disabled
              ></textarea>
            </div>
          </div>

          <div class="image-section-sell">
            <div class="columna2-sell">
              <div class="form_group_game_sell">
                <h3 class="message-image-sell">
                  La imagen que acompañara a la reseña se mostrará aquí:
                </h3>
              </div>
            </div>
            <div class="columna2-sell">
              <div class="image-preview-sell">
                <img id="preview-image_sell" :src="game.cover" />
              </div>
            </div>
          </div>

          <div class="submit_button_sell">
            <div class="form_group_game_sell">
              <button type="submit" class="btn-sell zoom-effect">
                Actualizar reseña
              </button>
            </div>
          </div>
        </form>
      </div>
    </template>
  </LayoutComponent>
</template>

<script>
import LayoutComponent from "@/components/Layout.vue";
import { verifier_login } from "@/services/login.api";
import {
  updateReview,
  confirmUpdateReview,
  getReviewById,
} from "@/services/review.api";

export default {
  name: "UpdateReviewView",
  components: {
    LayoutComponent,
  },
  async mounted() {
    await verifier_login();
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get("id");
    if (id) {
      const review = await getReviewById(id);
      this.game = review.game.game;
      this.platforms = review.game.game.platforms;
      this.platform_selected = review.review.platform;
      this.title = review.review.title;
      this.comment = review.review.comment;
      this.review_id = id;
    }
  },
  data() {
    return {
      game: {
        name: "",
        genres: [],
        platforms: [],
        cover: "",
        summary: "",
        involved_companies: [],
        release_year: "",
      },
      platforms: [],
      platform_selected: "",
      title: "",
      comment: "",
      review_id: "",
    };
  },
  methods: {
    async updateReview() {
      const urlParams = new URLSearchParams(window.location.search);
      const id = urlParams.get("id");
      const data = {
        platform: this.platform_selected,
        title: this.title,
        comment: this.comment,
      };
      const result = await confirmUpdateReview();
      if (result.isConfirmed) {
        await updateReview(id, data);
      }
    },
  },
};
</script>

<style>
@import url("../css/marketplace/upload_game.css");
</style>
