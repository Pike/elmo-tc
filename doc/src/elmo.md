# Elmo

The service that watches pulse gets the tree, and the JSON artifact. Based on
that data, it can publish the detailed data on ES, and create summary
information to enter into the elmo database.

As this service needs write access to the elmo database, it should be small, and
well audited.
