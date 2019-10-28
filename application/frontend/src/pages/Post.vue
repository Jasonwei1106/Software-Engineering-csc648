<template>
  <q-card class="q-pa-md" style="width: 98%; margin: 1em auto;">
    <strong>Post your DIY idea</strong>
    <hr>
    <q-form @submit.prevent.stop="onSubmit">
      <div class="q-pa-md">
          <div class="q-gutter-md">
          <div>
            <strong>Title:</strong>
            <q-input
              dense filled
              type="text"
              placeholder="What do you want to name your idea"
              v-model="poster.title"
              required
              style ="max-width: 300px;"
            >
              <template v-slot:prepend>
              </template>
            </q-input>
          </div>

          <div>
            <strong>Category:</strong>
              <q-select outlined
                v-model="poster.category"
                :options="options"
                :dense="dense"
                :options-dense="denseOpts"
                style="max-width: 300px;"
                >
                <template v-slot:prepend>
                </template>
              </q-select>
          </div>

          <div>
            <strong>Upload Your Picture</strong>
            <q-uploader
              label="Upload"
              auto-upload
              :url="getUrl"
              multiple
            />
          </div>

          <div>
            <strong>Discription</strong>
            <q-input
              dense filled
              type="textarea"
              placeholder="The discription of your project"
              v-model="poster.discprtion"
              required
              style ="max-width: 500px;"
            >
              <template v-slot:prepend>
              </template>
            </q-input>
          </div>

          <div>
            <strong>Material list:</strong>
            <div>
                <q-btn
                  icon="add"
                  @click="data.push({ material: '' })"
                />

                <div v-for="(val, ind) in data" :key="ind" >
                  <q-input
                    type = "text"
                    v-model="val.material"
                    style = "max-width: 500px;"
                  >
                  </q-input>
                <q-btn
                  icon="delete"
                  @click="data.splice(ind, 1)"
                />
              </div>
            </div>
          </div>

          <div>
            <strong> Add Your Steps Here:</strong>
              <div>
                <q-btn
                  icon="add"
                  @click="data.push({ step: '' })"
                />

                <div v-for="(val, ind) in data" :key="ind" >
                  <q-input
                    type = "textarea"
                    v-model="val.step"
                    style = "max-width: 500px;"
                  >
                  </q-input>
                <q-btn
                  icon="delete"
                  @click="data.splice(ind, 1)"
                />
              </div>
            </div>

          </div>
        </div>
      </div>

      <div class="q-gutter-sm" align="center" >
        <q-btn no-caps type="submit" color="primary" label="Confirm" />
      </div>
    </q-form>
  </q-card>
</template>

<script>
// import md5 from 'md5'

export default {
  data () {
    return {
      poster: {},
      options: [
        'Craft', 'Cooking', 'Tech', 'Workshop', 'Home&Decor'
      ],
      data: [
        {
          material: '',
          step: ''
        }
      ]
    }
  },
  methods: {
    getUrl (files) {
      return `http://localhost:4444/upload?count=${files.length}`
    }
  }
}
</script>
