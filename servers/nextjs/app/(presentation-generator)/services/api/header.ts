export const getHeader = () => {
  return {
    "Content-Type": "application/json",
    Accept: "application/json",  
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
  };
};

export const getHeaderForFormData = () => {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
<<<<<<< HEAD
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
=======
    "Access-Control-Allow-Headers": "Authorization",
>>>>>>> 78e1006 (Initial: presenton)
  };
};
