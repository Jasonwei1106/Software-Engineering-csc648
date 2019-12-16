<template>
  <div class="q-pa-md">
    <strong style="font-size: 200%;">
      {{tutorial.title}}
    </strong>

    <div class="row justify-start" style="margin:20px;">
      <q-img
        :src="tutorial.img"
        style="max-width: 200px; height: 150px; align: left; vertical-align: top; border: solid black 1px;"
      />

      <div class="column">
        <strong class="col-2" style="margin-left:10px;">
          Description
        </strong>

        <span class="col" style="padding-left: 30px;">
          {{ tutorial.description }}
        </span>
      </div>
    </div>

    <div>
      <q-expansion-item
        expand-separator default-opened
        icon="list" label="Material list"
        style="max-width: 400px; padding: 10px;"
      >
        <q-list dense bordered padding class="rounded-borders">
          <q-item
            v-for="(material, ind) in materials.items"
            :key="ind"
          >
            <q-item-section>
              {{ ind + 1 }}.  {{ material }}
            </q-item-section>
          </q-item>
        </q-list>
      </q-expansion-item>
    </div>

    <div class="q-pa-md" style="max-width: 650px;">
      <strong>Steps</strong>

      <q-list>
        <q-item
          v-for="(step, ind) in steps.contents"
          :key="ind"
        >
          <q-item-section style="max-width:20px">
            {{ ind + 1 }}.
          </q-item-section>

          <q-item-section top thumbnail class="q-ml-none">
            <img src="https://cdn.quasar.dev/img/mountains.jpg">
          </q-item-section>

          <q-item-section>
            <q-item-label style="padding:10px;">
              {{ step }}
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </div>

    <div>
      <strong class="q-pr-sm">Level of Difficulty: </strong>
      {{ tutorial.difficulty }}
    </div>

    <div>
      <q-btn
        label="EDIT"
        style="margin-right: 400px"
        @click="gotopost"
      />

      <q-btn
        label="Done"
        @click="gototutorial"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  created () {
    this.tutorial = this.$q.localStorage.getItem('__diyup__poster')
    this.materials = this.$q.localStorage.getItem('__diyup__material')
    this.steps = this.$q.localStorage.getItem('__diyup__step')
    this.$q.localStorage.remove('__diyup__poster')
    this.$q.localStorage.remove('__diyup__material')
    this.$q.localStorage.remove('__diyup__step')
  },
  // name: 'Tutorial page',
  data () {
    return {
      tutorial: null,
      materials: null,
      steps: null
    }
  },
  methods: {
    gototutorial: function () {
      let headers = {
        'x-access-token': this.$q.localStorage.getItem('__diyup__signedIn')
      }

      axios.post('http://54.67.109.241:5000/api/tutorial/create', {
        title: this.tutorial.title,
        image: 'test.png',
        category: this.tutorial.category,
        description: this.tutorial.description,
        author_difficulty: this.tutorial.difficulty
      }, { headers })
        .then(res => {
          let path1 = `http://54.67.109.241:5000/api/step/${res.data.token}/create`
          let path2 = `http://54.67.109.241:5000/api/items/${res.data.token}/create`
          let promises = []

          promises.push(axios.post(path1,
            {
              content: this.steps.contents,
              image: this.steps.images
            }, { headers }))
          promises.push(axios.post(path2, {
            name: this.materials.items,
            category: this.materials.categories,
            link: this.materials.links
          }, { headers }))

          Promise.all(promises).then(res => {
            this.$router.push({ name: 'rootHome' })
          })
        })

        .catch(err => {
          if (err) {
            this.$q.notify({
              icon: 'warning',
              color: 'negative',
              message: 'Something went wrong!'
            })
          }
        })
    },
    gotopost: function () {
      this.$q.localStorage.set('__diyup__edittutorial', this.tutorial)
      this.$q.localStorage.set('__diyup__editmaterial', this.materials)
      this.$q.localStorage.set('__diyup__editstep', this.steps)
      this.$router.push({ path: '/post' }).catch(err => {
        if (err) {
          this.$router.go()
        }
      })
    }
  }
}
</script>
