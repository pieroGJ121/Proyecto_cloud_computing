<template>
  <LayoutComponent>
    <template #Content>
      <div class="main-container-market">
        <h1>
          Desde aquí podras administrar todos los juegos que has publicado hasta
          ahora 🤑
        </h1>
        <div class="tabla-market">
          <table>
            <thead>
              <tr>
                <th>Imagen</th>
                <th>¿Vendido?</th>
                <th>Detalles</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <div class="image-preview-market">
                    <img id="preview-image-market" src="" />
                  </div>
                  <div class="image-section-market">
                    <div class="form_group_game_market">
                      <label for="image_upload" class="label-market"></label>
                      <input
                        type="file"
                        id="image_upload_market"
                        accept="image/*"
                        style="display: none"
                        required
                      />
                    </div>
                  </div>
                </td>
                <td>
                  <h2>Si</h2>
                </td>
                <td>
                  <div class="form_group_game_market">
                    <label for="name" class="label-market"
                      >NOMBRE DEL JUEGO</label
                    >
                    <input
                      type="text"
                      id="name"
                      class="form_control_game_market"
                      required
                    />
                  </div>
                  <div class="form_group_game_market">
                    <label for="price" class="label-market">PRECIO - S/</label>
                    <input
                      type="number"
                      id="price"
                      class="form_control_game_market"
                      required
                    />
                  </div>
                  <div class="form_group_game_market">
                    <label for="genre" class="label-market">GÉNERO</label>
                    <div class="custom-select-market">
                      <select
                        id="genre"
                        class="form_control_game_market"
                        required
                      >
                        <option value="" selected disabled hidden>
                          Selecciona un género
                        </option>
                        <option value="Accion">Accion</option>
                        <option value="Aventura">Aventura</option>
                        <option value="Retro">Retro</option>
                        <option value="Terror">Terror</option>
                      </select>
                    </div>
                  </div>
                  <div class="form_group_game_market">
                    <label for="platforms">PLATAFORMAS</label>
                    <div class="custom-select-market">
                      <select
                        id="platforms"
                        class="form_control_game_market"
                        required
                      >
                        <option value="" selected disabled hidden>
                          Selecciona una plataforma
                        </option>
                        <option value="PC">PC</option>
                        <option value="PlayStation">PlayStation</option>
                        <option value="Xbox">Xbox</option>
                        <option value="Nintendo Switch">Nintendo Switch</option>
                      </select>
                    </div>
                  </div>
                  <div class="form_group_game_market">
                    <label for="release_date">FECHA DE LANZAMIENTO</label>
                    <input
                      type="date"
                      id="release_year"
                      class="form_control_game_market"
                      required
                    />
                  </div>
                  <div class="form_group_game_market">
                    <label for="publisher" class="label-market">EDITOR</label>
                    <div class="custom-select-market">
                      <select
                        id="publisher"
                        class="form_control_game_market"
                        required
                      >
                        <option value="" selected disabled hidden>
                          Selecciona un editor
                        </option>
                        <option value="TAKE TWO INTERACTIVE">
                          TAKE TWO INTERACTIVE
                        </option>
                        <option value="Xbox Game Studios">
                          Xbox Game Studios
                        </option>
                        <option value="Valve">Valve</option>
                        <option value="Ubisoft">Ubisoft</option>
                      </select>
                    </div>
                  </div>
                  <div class="form_group_game_market">
                    <label for="synopsis-market" class="label-market"
                      >SINOPSIS (250 PALABRAS MÁXIMO)</label
                    >
                    <textarea
                      id="synopsis"
                      class="form_control_game_market"
                      required
                    ></textarea>
                  </div>
                </td>
                <td>
                  <div class="buttons-market">
                    <button id="update-market" onclick="updateRow(this)">
                      Actualizar
                    </button>
                    <button id="delete-market" onclick="deleteRow(this)">
                      Eliminar
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="info-market">
        <h3>Hasta ahora has publicado 5 juegos</h3>
        <h3>En total has recaudado: S/ 40.73</h3>
      </div>
    </template>
  </LayoutComponent>
</template>

<script>
import LayoutComponent from "@/components/Layout.vue";
import { verifier_login } from "@/services/login.api";
import { getSales } from "@/services/seller.api";

export default {
  name: "MarketplaceView",
  components: {
    LayoutComponent,
  },
  async mounted() {
    await verifier_login();
    await getSales();
  },
};
</script>

<style>
@import url("../css/marketplace/update_game.css");
</style>
