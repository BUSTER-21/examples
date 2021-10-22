const axios = require('axios');
const async = require('async');
const log4js = require('log4js');

const NANO_URL = process.env.NANO_URL;
const NANO_USERNAME = process.env.NANO_USERNAME;
const NANO_PASSWORD = process.env.NANO_PASSWORD;
const graphId = 'vibration-kurtosis-acceleration'

const DATA_FETCH_INTERVAL = 12*60*60;
var startTime = parseInt(Date.now()/1000) - DATA_FETCH_INTERVAL;

const logger = log4js.getLogger();
logger.level = "info";

const getISOString = function(t){
	return new Date(t).toISOString();
}

const getUrl = function(url){
	return [url].join('/');
}

const get = function(url, token, params, done){

	axios({
	  method: 'get',
	  url: NANO_URL + getUrl(url),
	  headers: {
	  	'Content-Type': 'application/json',
	  	'Accept': 'application/json',
	  	'Authorization': 'Bearer '+token
	  },
	  params: params || {}
	}).then(function (response) {
    logger.info(url, response.status);
		if(response.status !== 200){
			logger.error('Error making get call: '+url);
			return done(response.data, null);
		} else {
			return done(null, response.data);
		}
  }).catch(function (error) {
  	logger.error('Error making get call: '+url, error);
    return done(error, null);
  });
};

const post = function(url, token, data, done){
	return axios({
	  method: 'post',
	  url: NANO_URL + url,
	  headers: {
	  	'Content-Type': 'application/json',
	  	'Authorization': 'Bearer '+token
	  },
	  data: data
	}).then(function (response) {
    logger.info(url, response.status);
		if(response.status !== 200){
			logger.error('Error making post call: '+url);
			return done(response.data, null);
		} else {
			return done(null, response.data);
		}
  }).catch(function (error) {
  	logger.error('Error making post call: '+url, error);
    return done(error, null);
  });
};

const getToken = function(done){
	return post('/auth', '', { "username": NANO_USERNAME, "password": NANO_PASSWORD },function(e, r){
		if(e) {
			logger.error('Error authentication. Please check NANO_URL, NANO_USERNAME and NANO_PASSWORD');
			return done('ErrorAuth', null);
		} else {
			if(!r['token']){
				logger.error('Error authentication. Please check NANO_URL, NANO_USERNAME and NANO_PASSWORD');
				return done('ErrorAuth', null);
			} else {
				return done(null, r['token']);
			}
		}
	});
};

const getAssets = function(token, done){
	return get('/asset', token, {}, function(e, r){
		if(e) {
			return done(e, null);
		} else {
			// console.log(JSON.stringify(r, null, 2))
			logger.info("Assets found: "+r.length);
			return done(null, r);
		}
	});
};


const getData = function(token, stream, done){
	return post('/analytics/graph', token, 
		{'timestampFrom': startTime, 'timestampTo': startTime + DATA_FETCH_INTERVAL - 1, 'graphId': graphId, 'tagIdList': [stream]},
		function(e, r){
			if(e) {
				return done(e, null);
			} else {
				return done(null, r);
			}
		}
	);
};

// setInterval(function(){
	return getToken(function(e, token){
		if(e)
			return;
		else {
			console.log(token);
			return getAssets(token, function(e, assets){
				if(e){
					logger.error('Error fetching assets');
					return;
				}
				else {
					return async.eachLimit(assets, 10, function(stream, cb){
						logger.info('Fetching data for asset: '+stream.tagId);
						return getData(token, stream.tagId, function(e, r){
							if(e)
								logger.error('Error fetching data for stream: '+stream.tagId);
							else{
								console.log(JSON.stringify(r)); //data per asset and metric
							}
							return cb(null, null);
						});
					}, function(e, r){
						startTime += DATA_FETCH_INTERVAL;
						return;
					});
				}
			})
		}
	})
// }, DATA_FETCH_INTERVAL);