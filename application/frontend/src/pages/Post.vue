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

            <!-- <div>
              <q-uploader
                auto-upload
                color="dark" class="full-width"
                label="Upload Main Image"
                v-model="poster.img"
                :url="getUrl"
              />
            </div> -->

            <div>
              <q-input
                dense outlined required
                type="textarea"
                label="Description"
                placeholder="Tutorial description goes here..."
                v-model="poster.description"
              />
            </div>

            <div>
              <q-badge color="primary">
                Difficulty Rating: {{ poster.difficulty || 1 }} (1 to 5)
              </q-badge>
              <q-slider
                markers
                v-model="poster.difficulty"
                :min="1" :max="5"
              />
            </div>

            <div>
              <strong>Material List:</strong>

              <div class="row q-gutter-sm q-mb-sm">
                <q-input
                  dense outlined
                  class="col"
                  type="text" placeholder="Put your tools here. ie) Egg x 2"
                  v-model="materialInput"
                />

                <q-btn
                  class="col-2"
                  label ="Add" color="dark"
                  @click="addList"
                />
              </div>

              <q-list
                bordered separator
                v-if="materials.items.length > 0"
              >
                <q-item
                  v-for="(material, ind) in materials.items"
                  :key="ind"
                  dense
                >
                  <q-item-section>
                    {{ material }}
                  </q-item-section>

                  <q-btn
                    round flat
                    icon="delete"
                    @click="materials.items.splice(ind, 1)"
                  />
                </q-item>
              </q-list>
            </div>

            <div>
              <strong>Step List:</strong>

              <div class="row q-gutter-sm q-mb-sm">
                <q-input
                  dense outlined
                  class="col" type="textarea"
                  placeholder="Step description goes here."
                  v-model="stepInput"
                />

                <q-btn
                  class="col-2"
                  label="add" color="dark"
                  @click="addStep"
                />
              </div>

              <q-list
                bordered separator
                v-if="steps.contents.length > 0"
              >
                <q-item
                  v-for="(step, ind) in steps.contents"
                  :key="ind"
                  dense
                  style="overflow-wrap: break-word;"
                >
                  <q-item-section>
                    {{ step }}
                  </q-item-section>

                  <q-btn
                    round flat
                    icon="delete"
                    @click="steps.contents.splice(ind, 1)"
                  />
                </q-item>
              </q-list>
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
      this.$q.localStorage.remove('__diyup__edittutorial')
      this.$q.localStorage.remove('__diyup__editmaterial')
      this.$q.localStorage.remove('__diyup__editstep')
    }
  },
  data () {
    return {
      materialInput: '',
      stepInput: '',
      poster: {
        img: 'testimg'
      },
      options: [
        { label: 'Electronics', value: 'electronics' },
        { label: 'Coding', value: 'coding' },
        { label: 'Robotics', value: 'robotics' },
        { label: 'Cooking', value: 'cooking' },
        { label: 'Crafts', value: 'crafts' },
        { label: 'Home & Decor', value: 'homeDecor' },
        { label: 'Testing', value: 'testing' }
      ],
      materials: {
        items: [],
        categories: [],
        links: []
      },
      steps: {
        contents: [],
        images: []
      }
    }
  },
  methods: {
    onSubmit: function () {
      this.poster.difficulty = this.poster.difficulty || 1
      this.poster.difficulty = Number(this.poster.difficulty)

      if (this.steps.contents.length === 0 || this.materials.items.length === 0) {
        this.$q.notify({
          icon: 'warning',
          color: 'negative',
          message: 'put your steps and materials'
        })
      } else {
        this.$q.localStorage.set('__diyup__poster', this.poster)
        this.$q.localStorage.set('__diyup__material', this.materials)
        this.$q.localStorage.set('__diyup__step', this.steps)
        this.$router.push({ path: '/preview' }).catch(err => {
          if (err) {
            this.$router.go()
          }
        })
      }
    },
    getUrl (files) {
      axios.post('https://api.imgur.com/3/image/', {
        image: files
      }).then(res => {
      })
    },
    addList () {
      this.materials.items.push(this.materialInput)
      this.materials.categories.push('tools')
      this.materials.links.push('amazon.com')
      this.materialInput = ''
    },
    addStep () {
      this.steps.contents.push(this.stepInput)
      this.steps.images.push('test.png')
      this.stepInput = ''
    }
  }
}
</script>
