const get = {
    async getmovies(){
        try{
            const res = await fetch("http://127.0.0.1:8000/");
            return res;
        }catch(e){
            console.log(e);
        }
    },
    async getrecommendations(movies){
        try{
            const res = await fetch(`http://127.0.0.1:8000/recommend/${movies}`);
            return res;
        }catch(e){
            console.log(e);
        }
    },
    async getsearchres(movies){
        try{
            const res = await fetch(`http://127.0.0.1:8000/search/${movies}`);
            return res;
        }catch(e){
            console.log(e);
        }
    }
}

export default get;