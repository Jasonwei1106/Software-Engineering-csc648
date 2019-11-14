<template>
  <div class="q-pa-md">
  <Strong style="font-size: 200%;"> {{tutorial.title}} </Strong>
    <div
      class= "row justify-start"
      style="margin:20px;"
    >
      <q-img
        :src="tutorial.url"
        style="max-width: 200px; height: 150px; align: left; vertical-align: top; border: solid black 1px;"
      />
      <div class="column">
      <strong class="col-2" style="margin-left:10px;">Description</strong>
      <span class="col" style="padding-left: 30px;"> {{tutorial.description}}</span>
      </div>
    </div >
    <div>
      <q-expansion-item
        expand-separator
        icon="list"
        label="Material list"
        style="max-width: 400px; padding: 10px;"
        default-opened
      >
        <q-list dense bordered padding class="rounded-borders">
          <q-item
            v-for="(material, ind) in materials"
            :key="ind"
          >
            <q-item-section>
              {{ind+1}}.  {{material}}
            </q-item-section>
          </q-item>
        </q-list>
      </q-expansion-item>
    </div>
    <div class="q-pa-md" style="max-width: 650px;">
      <strong>Steps</strong>
      <q-list>
          <q-item
            v-for="(step, ind) in steps"
            :key="ind"
          >
            <q-item-section style="max-width:20px"> {{ind+1}}.  </q-item-section>
            <q-item-section top thumbnail class="q-ml-none">
              <img src="https://cdn.quasar.dev/img/mountains.jpg">
            </q-item-section>
            <q-item-section>
              <q-item-label style="padding:10px;">{{step}}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
    </div>
    <div>
      <q-btn
        label="EDIT"
        style="margin-right: 400px"
      />
      <q-btn
        label="Done"
      />
    </div>
  </div>
</template>

<script>
export default {
  created () {
    this.tutorial = this.$q.localStorage.getItem('__diyup__poster')
    this.materials = this.$q.localStorage.getItem('__diyup__material')
    this.steps = this.$q.localStorage.getItem('__diyup__step')
    console.log(this.poster)
  },
  // name: 'Tutorial page',
  data () {
    return {
      tutorial: null,
      materials: null,
      steps: null
    }
  }
}
</script>
