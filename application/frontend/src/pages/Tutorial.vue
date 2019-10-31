<template>
  <div class="q-pa-md">
  <Strong style="font-size: 200%;"> tutorial.title </Strong>
  <div>
    <q-expansion-item
          expand-separator
          icon="list"
          label="Material list"
          style="max-width: 500px; padding: 10px;"
    >
      <q-list dense bordered padding class="rounded-borders">
        <q-item
          v-for="(list, ind) in tutorial.lists"
          :key="ind"
        >
          <q-item-section>
            {{list}}
          </q-item-section>
        </q-item>
      </q-list>
    </q-expansion-item>
  </div>
  <div class="q-pa-md" style="max-width: 650px;">
    <q-list>
        <q-item
          v-for="(step, ind) in tutorial.steps"
          :key="ind"
        >
          <q-item-section top thumbnail class="q-ml-none">
            <img src="https://cdn.quasar.dev/img/mountains.jpg">
          </q-item-section>
          <q-item-section>
            <q-item-label>{{step.name}}</q-item-label>
            <q-item-label caption>{{step.content}}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
  </div>
   <div>
    <Comment />
  </div>
  </div>
</template>

<script>
import Comment from '../pages/Comments'
export default {
  name: 'Tutorial page',
  data () {
    return {
      lorem: 'Lorem ipsum dolor sit amet, consectetur',
      tutorial: {
        title: 'First DIY',
        lists: [
          '1',
          '2'
        ],
        steps: [
          {
            name: 'S1',
            content: 'what to do'
          },
          {
            name: 'S2',
            content: 'what to do next'
          }
        ]
      }
    }
  },
  components: {
    Comment
  }
}
</script>
