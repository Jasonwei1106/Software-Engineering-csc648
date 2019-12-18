<template>
  <div>
      <!-- title="DIYup Tutorials" -->
    <q-table
      flat hide-header wrap-cells
      separator="none"
      row-key="title"
      :data="curData"
      :columns="columns"
      :filter="option.value"
      :pagination.sync="pagination"
    >
      <template v-slot:top-left>
        <q-btn
          v-if="$q.localStorage.has('__diyup__signedIn')"
          outline
          label="Create a new project"
          @click="goToPost"
        />
        <q-btn
          v-else
          outline
          label="Please sign in to create tutorials"
          @click="icon = true"
        />
      </template>

      <template v-slot:top-right>
        <q-toolbar>
          <q-btn
            v-if="option !== ''"
            flat dense round
            class="q-mr-sm"
            icon="close"
            @click="option = ''"
          />
          <q-select
            outlined dense
            class="col-4" label="Category Filter"
            bg-color="white" color="black"
            v-model="option"
            style="min-width: 200px;"
            :options="categories"
          />
        </q-toolbar>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td colspan="100%" key="title" :props="props">
            <q-card class="q-pa-md" style="min-height: 15vh;">
              <div
                class="row cursor-pointer"
                @click="routeToTutorial(props.row)"
              >
                <div class="col-4" align="center">
                  <q-img
                    :src="
                      'https://placeimg.com/500/300/nature?t=' + Math.random()
                    "
                    spinner-color="primary"
                    style="max-height: 140px; max-width: 150px"
                  />
                </div>
                <div class="col gt-xs">
                  <b>Title:</b>
                  {{ props.row.title }} by {{ props.row.author_username }}<br>

                  <b>Author's Difficulty Rating:</b>
                  {{ props.row.author_difficulty }}<br>

                  <!-- <b>Users' Difficulty Rating:</b>
                  {{ props.row.viewer_difficulty === 'None' ? props.row.author_difficulty : props.row.viewer_difficulty }}<br> -->

                  <b>Users' Rating:</b>
                  <q-rating
                    readonly
                    class="q-pl-sm" size="1.5em" icon="thumb_up"
                    :value="
                      props.row.rating === 'None' ? 5.0 : Number(props.row.rating)
                    "
                  />
                  <br>

                  <b>Category:</b>
                  {{ props.row.category }}<br>
                </div>

                <div class="col-5 q-pr-xl gt-xs" align="left">
                  <b>Description:</b> {{ props.row.description }}
                </div>

                <div class="col q-pl-xs xs" align="left">
                  <b>Title:</b>
                  {{ props.row.title }} by {{ props.row.author_username }}
                  <br>

                  <b>Description:</b> {{ props.row.description }}
                </div>
              </div>
            </q-card>
          </q-td>
        </q-tr>
      </template>
    </q-table>

    <q-dialog v-model="icon">
      <q-card >
        <LogIn @close="icon = false" />
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import LogIn from '../components/Login'

export default {
  watch: {
    $route: 'titleQueryFilter'
  },
  components: {
    LogIn
  },
  created () {
    this.fetchData()
    this.filter = this.$route.query.title || ''
  },
  data () {
    return {
      icon: false,
      filter: '',
      categories: [
        { label: 'Electronics', value: 'electronics' },
        { label: 'Coding', value: 'coding' },
        { label: 'Robotics', value: 'robotics' },
        { label: 'Cooking', value: 'cooking' },
        { label: 'Crafts', value: 'crafts' },
        { label: 'Home & Decor', value: 'homeDecor' },
        { label: 'Testing', value: 'testing' }
      ],
      option: '',
      columns: [
        {
          name: 'title',
          label: 'Title',
          required: true,
          align: 'left',
          field: row => row.title,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: 'category',
          label: `Category`,
          required: true,
          align: 'left',
          field: row => row.category,
          format: val => `${val}`,
          sortable: true
        }
      ],
      data: [],
      curData: [],
      pagination: {
        rowsPerPage: 10,
        sortBy: 'title',
        descending: false
      }
    }
  },
  methods: {
    routeToTutorial: function (entry) {
      this.$router.push(`/tutorial/${entry.uuid}`)
    },
    titleQueryFilter: function () {
      this.filter = this.$route.query.title
      if (this.filter) {
        this.curData = this.data.filter(v => v.title.toLowerCase().includes(this.filter.toLowerCase()))
      } else {
        this.curData = this.data
      }
    },
    fetchData: function () {
      axios.get('http://54.67.109.241:5000/api/tutorial/get')
        .then(res => {
          this.data = res.data.tutorials
          this.data.forEach(element => {
            this.curData.push(element)
          })

          // console.log(this.data)
        })
    },
    goToPost: function () {
      if (this.$q.localStorage.has('__diyup__signedIn')) {
        this.$router.push({ path: '/post' }).catch(err => {
          if (err) {
            // error
          }
        })
      }
    }
  }
}
</script>

<style lang="stylus">
.my-table-details {
  font-size: 0.85em;
  font-style: italic;
  max-width: 200px;
  white-space: normal;
  color: #555;
  margin-top: 4px;
}
</style>
