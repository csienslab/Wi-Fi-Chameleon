export default (state = {}, action) => {
  switch(action.type) {
    case 'LOGIN':
      return {
        token: action.token,
        name: action.name,
        email: action.email,
        id: action.id
      };
    case 'LOGOUT':
      return {};
    default:
      return state;
  };
};