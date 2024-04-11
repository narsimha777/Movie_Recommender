import React, { useState } from "react";
import get from "../utils/get";

const Search = () => {
    const [name, setName] = useState();
    const [res, setRes] = useState();
    const [reco, setRec] = useState({});
    const handleSubmit = async (e) => {
        e.preventDefault();
        const r = await get.getsearchres(name);
        const rstr = await r.json();
        // console.log(rstr);
        setRes(rstr);
        // console.log(res[0].title);
    }
    const getRecomendations = async (movie) => {
        try {
            const res = await get.getrecommendations(movie);
            const restr = await res.json(); 
            const updatedobj = {...reco}
            updatedobj[movie] = restr.recommended_movies; 
            setRec(updatedobj);
            console.log(reco);
        } catch (error) {
            console.error('Error fetching recommendations:', error);
        }
    }    
    return (
        <div className="max-w-lg mx-auto mt-10 p-6 bg-gray-100 rounded-lg shadow-md">
            <form onSubmit={handleSubmit} className="mb-4">
                <label className="block mb-2 text-lg font-semibold text-gray-800">
                    Movie:
                </label>
                <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter Movie name to get similar Recommendations"
                    className="w-full px-4 py-2 text-lg border border-gray-300 rounded-md focus:outline-none focus:border-blue-500"
                />
                <button
                    type="submit"
                    className="mt-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
                >
                    Submit
                </button>
            </form>
            <div className="bg-white rounded-lg shadow-md">
                {res &&
                    res.map((movie) => (
                        <div key={movie.title} className="p-4 border-b border-gray-200">
                            <h1 className="text-xl font-semibold text-gray-800">
                                <em>Movie:</em> {movie.title}
                            </h1>
                            <div className="mt-2">
                                <h2 className="text-lg font-semibold text-gray-700">
                                    <em>Crew:</em>
                                </h2>
                                {movie.crew.map((member, index) => (
                                    <p key={index} className="text-gray-600">
                                        {member}
                                    </p>
                                ))}
                            </div>
                            <div className="mt-2">
                                <h2 className="text-lg font-semibold text-gray-700">
                                    <em>Members:</em>
                                </h2>
                                {movie.cast.map((member, index) => (
                                    <p key={index} className="text-gray-600">
                                        {member}
                                    </p>
                                ))}
                            </div>
                            <button
                                onClick={() => {
                                    console.log("Clicked on movie:", movie.title);
                                    getRecomendations(movie.title);
                                }}
                                className="mt-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
                            >
                                Get Recommendations
                            </button>
                            {reco[movie.title] && (<>
                                <h1 className="text-xl font-semibold text-gray-800">
                                    <em>Recommendations for Movie:</em><p className="text-yellow-500">{movie.title}</p>
                                </h1>
                                {reco[movie.title].map((member, index) => (
                                    <p key={index} className="text-green-600">
                                        {member}
                                    </p>
                                ))}
                            </>)}
                        </div>
                    ))}
            </div>
        </div>
    );
}

export default Search;