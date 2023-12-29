import { createStore } from "vuex";
import { auth } from "./auth.module";
import { test } from "./test.module";

const store = createStore({
  modules: {
    auth,
    test,
  },
});

export default store;
