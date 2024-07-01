import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        numItems: {{ cart.get_total_length }},
        totalCost: {{ cart.get_total_cost }},
        cartItems: []
    },
    mutations: {
        increment(state, quantity) {
            state.numItems += quantity;
        },
        changeTotalCost(state, newCost) {
            state.totalCost += newCost
        }
    }
})
