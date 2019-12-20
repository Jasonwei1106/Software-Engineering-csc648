<template>
  <div
    class="q-pa-md shadow-2"
    style="
      width: 98%;
      max-width: 1000px;
      margin: 1em auto;
      border-radius: 3px;
    "
  >
    <div align="center">
      <Strong style="font-size: 200%;">{{ data.title }}</Strong>
      <q-separator color="dark" />
    </div>

    <div class="xs">
      <div class="q-pa-md">
        <q-img
          placeholder-src="https://placeimg.com/500/300/nature"
          :src="'https://placeimg.com/500/300/nature=t' + Math.random()"
          style="
            max-height: 150px;
            align: left;
            vertical-align: top;
            border: solid black 1px;
          "
        />
      </div>

      <div
        align="center"
        class="bg-primary text-white"
        style="border-radius: 3px; width: 92%; margin: 0 auto;"
      >
        <strong>Level of Difficulty:</strong>
        {{ data.difficulty }}
      </div>
    </div>

    <!-- ---------- IMAGE CODEBLOCK ---------- -->
    <div class="row q-pa-md">
      <div class="col-4 gt-xs">
        <q-img
          placeholder-src="https://placeimg.com/500/300/nature"
          :src="'https://placeimg.com/500/300/nature=t' + Math.random()"
          style="
            max-height: 300px;
            align: left;
            vertical-align: top;
            border: solid black 1px;
          "
        />
        <div
          align="center"
          class="q-mt-xs bg-primary text-white"
          style="border-radius: 3px;"
        >
          <strong>Level of Difficulty:</strong>
          {{ data.difficulty }}
        </div>
      </div>

      <div class="col q-pl-md">
        <strong class="text-h4">
          Description
          <q-separator color="dark" />
        </strong>
        <div class="q-px-lg q-my-sm">
          {{ data.description }}
        </div>
      </div>
    </div >

    <!-- ---------- MATERIAL LIST CODEBLOCK ---------- -->
    <div>
      <q-expansion-item
        expand-separator
        icon="list"
        label="Material list"
        style="padding: 10px;"
        default-opened
      >
        <q-list dense bordered padding class="rounded-borders">
          <q-item
            v-for="(list, ind) in materials.items"
            :key="ind"
          >
            <q-item-section>
              {{ ind + 1 }}.  {{ list }}
            </q-item-section>
          </q-item>
        </q-list>
      </q-expansion-item>
    </div>

    <!-- ---------- STEP CODEBLOCK ---------- -->
    <div class="q-pa-md">
      <strong class="text-h4">
        Steps
        <q-separator color="dark" />
      </strong>
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
            <q-item-label style="padding:10px;">{{ step }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </div>

    <div class="row">
      <q-btn
        outline no-caps
        class="col-3" label="Edit"
        @click="gotopost"
      />

      <q-space />

      <q-btn
        outline no-caps
        class="col-3" label="Publish"
        @click="gototutorial"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  created () {
    this.data = this.$q.localStorage.getItem('__diyup__poster')
    this.materials = this.$q.localStorage.getItem('__diyup__material')
    this.steps = this.$q.localStorage.getItem('__diyup__step')
    this.$q.localStorage.remove('__diyup__poster')
    this.$q.localStorage.remove('__diyup__material')
    this.$q.localStorage.remove('__diyup__step')
  },
  // name: 'Tutorial page',
  data () {
    return {
      data: null,
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
        title: this.data.title,
        image: 'test.png',
        category: this.data.category,
        description: this.data.description,
        author_difficulty: this.data.difficulty
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
      this.$q.localStorage.set('__diyup__edittutorial', this.data)
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
