CREATE ROLE nagios_ro LOGIN PASSWORD 'nagios_dev';
GRANT USAGE ON SCHEMA veille TO nagios_ro;
GRANT SELECT ON veille.digests TO nagios_ro;
