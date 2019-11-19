<template>
<div style="width:800px; margin:0 auto">
  <q-card class="q-pa-md" style="width: 98%; margin: 1em auto;">
    <strong><font size="10">Post your DIY idea</font></strong>
    <hr>
    <q-form @submit.prevent.stop="onSubmit">
      <div class="q-pa-md">
          <div class="q-gutter-md">
          <div>
            <strong>Title:</strong>
            <q-input
              filled
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
              v-model="poster.img"
              multiple
            />
          </div>

          <div>
            <strong>Discription</strong>
            <q-input
              dense filled
              type="textarea"
              placeholder="The discription of your project"
              v-model="poster.description"
              required
              style ="max-width: 500px;"
            >
              <template v-slot:prepend>
              </template>
            </q-input>
          </div>
          <div>
            <strong>Material list:</strong>
            <div class ="flex">
              <q-input
                dense filled
                type="text"
                placeholder="Put your tools Here"
                v-model="materialinput"
                style ="max-width: 500px;"
              >
              </q-input>
              <q-btn
                label ="Add"
                @click="addlist"
              />
            </div>
            <q-item
              clickable
              style ="max-width: 400px;"
              v-for="(material, ind) in materials"
              :key="ind"
            >
              <q-item-section>
              {{material}}
              </q-item-section>
              <q-btn
                  icon="delete"
                  @click="materials.splice(ind, 1)"
                />
            </q-item>
          </div>
          <div>
            <div>
            </div>
          </div>

          <div>
            <strong> Add Your Steps Here:</strong>
              <div>
                <q-input
                dense filled
                type="textarea"
                placeholder="Put your description Here"
                v-model="stepinput"
                style ="max-width: 500px;"
                >
                </q-input>
                <q-btn
                  label="add"
                  @click="addstep"
                />
              </div>
              <q-item
              clickable
              v-for="(step, ind) in steps"
              :key="ind"
            >
              <q-item-section style="max-width: 400px; overflow-wrap: break-word;">
                {{step}}
              </q-item-section>
              <q-btn
                  icon="delete"
                  @click="steps.splice(ind, 1)"
                />
            </q-item>
          </div>
        </div>
      </div>

      <div class="q-gutter-sm" align="center" >
        <q-btn no-caps type="submit" color="primary" label="Confirm" />
      </div>
    </q-form>
  </q-card>
</div>
</template>

<script>

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
      materialinput: '',
      stepinput: '',
      poster: {},
      options: [
        'Craft', 'Cooking', 'Tech', 'Workshop', 'Home&Decor'
      ],
      materials: [
      ],
      steps: [
      ]
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
      return `http://localhost:4444/upload?count=${files.length}`
    },
    addlist () {
      this.materials.push(this.materialinput)
      this.materialinput = ''
    },
    addstep () {
      this.steps.push(this.stepinput)
      this.stepinput = ''
    }
  }
}
</script>
