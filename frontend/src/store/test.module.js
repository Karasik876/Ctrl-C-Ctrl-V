import TestService from '../services/test.service';

const initialState = {
  testsListAll: [],
  testCreated: false,
};

export const test = {
  namespaced: true,
  state: initialState,
  actions: {
    fetchTests({ commit }, user) {
      return TestService.fetchTests().then(
        testsList => {
          commit('fetchTestsSuccess', testsList);
          return Promise.resolve(testsList);
        },
        error => {
          commit('fetchTestsFailure');
          return Promise.reject(error);
        }
      );
    },
    addTest({ commit }, test) {
      return TestService.addTest(test).then(
        test => {
          commit('addTestSuccess');
          return Promise.resolve(test);
        },
        error => {
          commit('addTestFailure');
          return Promise.reject(error);
        }
      );
    },
  },
  mutations: {
    fetchTestsSuccess(state, test) {
      state.testsListAll = test;
    },
    fetchTestsFailure(state) {
      state.testsListAll = [];
    },
    addTestSuccess(state, testStatus) {
      state.testCreated = testStatus;
    },
    addTestFailure(state) {
      state.testCreated = false;
    },
  }
};
