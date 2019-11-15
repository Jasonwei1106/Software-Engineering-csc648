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
            v-for="(list, ind) in lists"
            :key="ind"
          >
            <q-item-section>
              {{ind+1}}.  {{list}}
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
      <Comment style="margin-top:25px"/>
    </div>
  </div>
</template>

<script>
import Comment from '../pages/Comments'
export default {
  created () {
    this.tutorial = this.$q.localStorage.getItem('__diyup__donetutorial')
    this.lists = this.$q.localStorage.getItem('__diyup__donematerial')
    this.steps = this.$q.localStorage.getItem('__diyup__donestep')
    console.log(this.steps)
  },
  components: {
    Comment
  }
}
</script>
