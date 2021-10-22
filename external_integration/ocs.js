const axios = require('axios');
const async = require('async');
const log4js = require('log4js');

const OCSUrl = process.env.OCS_URL;
const OCS_CLIENT_ID = process.env.OCS_CLIENT_ID;
const OCS_CLIENT_SECRET = process.env.OCS_CLIENT_SECRET;
const OCS_TENANT = process.env.OCS_TENANT;
const OCS_NAMESPACE = process.env.OCS_NAMESPACE;

const DATA_FETCH_INTERVAL = 12*60*60*1000;
var startTime = Date.now() - DATA_FETCH_INTERVAL;

const logger = log4js.getLogger();
logger.level = "info";

const getISOString = function(t){
	return new Date(t).toISOString();
}

const getUrl = function(url){
	return ['/api/v1/Tenants', OCS_TENANT, 'Namespaces', OCS_NAMESPACE, url].join('/');
}

const get = function(url, token, params, done){

	axios({
	  method: 'get',
	  url: OCSUrl + getUrl(url),
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

const post = function(url, done){

	const d = {
    'client_id': OCS_CLIENT_ID,
    'client_secret': OCS_CLIENT_SECRET,
    'grant_type': 'client_credentials'
  };
	const data = Object.keys(d).map((key) => `${key}=${encodeURIComponent(d[key])}`).join('&');
	console.log(data);

	return axios({
	  method: 'post',
	  url: OCSUrl + url,
	  headers: {
	  	'Content-Type': 'application/x-www-form-urlencoded'
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
	return post('/identity/connect/token', function(e, r){
		if(e) {
			logger.error('Error authentication. Please check ocs_url, client_id and client_secret');
			return done('ErrorAuth', null);
		} else {
			if(!r['access_token']){
				logger.error('Error authentication. Please check ocs_url, client_id and client_secret');
				return done('ErrorAuth', null);
			} else {
				return done(null, r['access_token']);
			}
		}
	});
};

const getStreams = function(token, done){
	return get('Streams', token, {}, function(e, r){
		if(e) {
			return done(e, null);
		} else {
			console.log(JSON.stringify(r, null, 2))
			return done(null, r);
		}
	});
};

const getStreamData = function(token, stream, done){
	return get('Streams/'+stream+'/Data', token, 
		{'startIndex': getISOString(startTime), 'endIndex': getISOString(startTime + DATA_FETCH_INTERVAL - 1)},
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
			return getStreams(token, function(e, streams){
				if(e){
					logger.error('Error fetching streams');
					return;
				}
				else {
					return async.eachLimit(streams, 10, function(stream, cb){
						logger.info('Fetching data for stream: '+stream.Id);
						return getStreamData(token, stream.Id, function(e, r){
							if(e)
								logger.error('Error fetching data for stream: '+stream.Id);
							else{
								r.forEach(function(e){
									e['Tag'] = stream.Id+'/'+stream.Name;
								});
								logger.info(r);
							}
							return cb(null, null);
						});
					}, function(e, r){
						startTime += DATA_FETCH_INTERVAL;
						return;
					})
				}
			})
		}
	})
// }, DATA_FETCH_INTERVAL);