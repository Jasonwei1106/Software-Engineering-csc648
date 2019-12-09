<template>
  <div style="max-width:800px; margin:0 auto">
    <div style="width: 98%; margin: 1em auto;">

      <q-form @submit.prevent.stop="onSubmit">
        <div class="q-pa-md">
          <div class="q-gutter-md">

            <div>
              <q-input
                required outlined
                type="text" label="Title"
                placeholder="What do you want to name your idea"
                v-model="poster.title"
              />
            </div>

            <div>
              <q-select
                outlined required
                label="Category"
                v-model="poster.category"
                :options="options"
              />
            </div>

            <div>
              <q-uploader
                auto-upload
                color="dark" class="full-width"
                label="Upload Main Image"
                v-model="poster.img"
                :url="getUrl"
              />
            </div>

            <div>
              <q-input
                dense outlined required
                type="textarea"
                Label="Description"
                placeholder="Tutorial description goes here..."
                v-model="poster.description"
              />
            </div>

            <div>
              <strong>Material List:</strong>

              <div class="row q-gutter-sm">
                <q-input
                  dense outlined
                  class="col"
                  type="text" placeholder="Put your tools Here"
                  v-model="materialInput"
                />

                <q-btn
                  class="col-2"
                  label ="Add" color="dark"
                  @click="addList"
                />
              </div>

              <q-item
                v-for="(material, ind) in materials"
                :key="ind"
                clickable
              >
                <q-item-section>
                  {{ material }}
                </q-item-section>

                <q-btn
                  icon="delete"
                  @click="materials.splice(ind, 1)"
                />
              </q-item>
            </div>

            <div>
              <strong>Step List:</strong>

              <div class="row q-gutter-sm">
                <q-input
                  class="col"
                  dense outlined
                  type="textarea"
                  placeholder="Put your description Here"
                  v-model="stepInput"
                />

                <q-btn
                  class="col-2"
                  label="add" color="dark"
                  @click="addStep"
                />
              </div>

              <q-item
                v-for="(step, ind) in steps"
                :key="ind"
                clickable
                style="overflow-wrap: break-word;"
              >
                <q-item-section>
                  {{ step }}
                </q-item-section>

                <q-btn
                  icon="delete"
                  @click="steps.splice(ind, 1)"
                />
              </q-item>
            </div>
          </div>

          <div class="q-mt-sm">
            <q-btn
              no-caps
              class="full-width" type="submit"
              color="primary" label="Confirm"
            />
          </div>
        </div>
      </q-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  created () {
    if (this.$q.localStorage.has('__diyup__edittutorial')) {
      this.poster = this.$q.localStorage.getItem('__diyup__edittutorial')
      this.materials = this.$q.localStorage.getItem('__diyup__editmaterial')
      this.steps = this.$q.localStorage.getItem('__diyup__editstep')
    }
  },
  data () {
    return {
      materialInput: '',
      stepInput: '',
      poster: {
        img: 'testimg',
        difficulty: '1'
      },
      options: [
        'Craft', 'Cooking', 'Tech', 'Workshop', 'Home&Decor'
      ],
      materials: [],
      steps: []
    }
  },
  methods: {
    onSubmit: function () {
      this.$q.localStorage.set('__diyup__poster', this.poster)
      this.$q.localStorage.set('__diyup__material', this.materials)
      this.$q.localStorage.set('__diyup__step', this.steps)
      this.$router.push({ path: '/preview' }).catch(err => {
        if (err) {
          this.$router.go()
        }
      })
    },
    getUrl (files) {
      axios.post('https://api.imgur.com/3/image/', {
        image: files
      }).then(res => {
        console.log(res)
      })
    },
    addList () {
      this.materials.push(this.materialInput)
      this.materialInput = ''
    },
    addStep () {
      this.steps.push(this.stepInput)
      this.stepInput = ''
    }
  }
}
</script>
