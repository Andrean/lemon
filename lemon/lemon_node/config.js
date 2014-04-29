var config	= {};

config.lemon	= {};
config.mongodb	= {};
config.webpersonal	= {};

config.lemon.server	= {};
config.lemon.server.hostname	= 'dev-lemon';
config.lemon.server.port	= 10003;

config.db	= 'mongodb://dev-lemon/lemon';

config.webpersonal.settingsPath	= 'D:/cfg';
config.webpersonal.gitPath		= 'C:\\Program Files (x86)\\Git\\cmd';

module.exports	= config;