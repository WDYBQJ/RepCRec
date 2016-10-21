# RepCRec
In groups of 1 or 2, you will implement a distributed database, complete with multiversion concurrency control, deadlock detection, replication, and failure recovery. If you do this project, you will have a deep insight into the design of a distributed system. Normally, this is a multi-year, multi-person effort, but it’s doable because the database is tiny.

Data
The data consists of 20 distinct variables x1, ..., x20 (the numbers between
1 and 20 will be referred to as indexes below). There are 10 sites
numbered 1 to 10. A copy is indicated by a dot. Thus, x6.2 is the copy of
variable x6 at site 2. The odd indexed variables are at one site each (i.e.
1 + index number mod 10 ). For example, x3 and x13 are both at site 4.
Even indexed variables are at all sites. Each variable xi is initialized to the
value 10i. Each site has an independent lock table. If that site fails, the
lock table is erased.
Algorithms to use
Please implement the available copies approach to replication using two
phase locking (using read and write locks) at each site and validation at
commit time. A transaction may read a variable and later write that same
variable as well as others. Please use the version of the algorithm specified
in my notes rather than in the textbook.
Detect deadlocks using cycle detection and abort the youngest transaction
in the cycle. This implies that your system must keep track of the
oldest transaction time of any transaction holding a lock. (We will ensure
that no two transactions will have the same age.)
Read-only transactions should use multiversion read consistency.
Test Specification
When we test your software, input instructions come from a file or the
standard input, output goes to standard out. (That means your algorithms
may not look ahead in the input.) Input instructions occurring in one step
begin at a new line and end with a carriage return. Thus, there may be
several operations in each step, though at most only one per transaction.
Some of these operations may be blocked due to conflicting locks. If an
operation for one transaction is forced to wait (because of blocking), that
does not affect the operations of other transactions. That is, you may assume
that all operations on a single line occur concurrently. When running our
tests, we will ensure that operations occurring concurrently don’t conflict
with one another. We will also ensure that when a transaction is waiting, it
will not receive another operation.
The execution file has the following format:
begin(T1) says that T1 begins
beginRO(T3) says that T3 begins and is read-only
R(T1, x4) says transaction 1 wishes to read x4 (provided it can get the
locks or provided it doesn’t need the locks (if T1 is a read-only transaction)).
It should read any up (i.e. alive) copy and return the current value (or the
value when T1 started for read-only transaction). It should print that value.
W(T1, x6,v) says transaction 1 wishes to write all available copies of x6
(provided it can get the locks) with the value v. If it can get the locks on
only some sites, it should get them. So T1 should obtain locks on all sites
that are up, that contain x6, and for which there is no conflicting lock on
x6. However T1 can write to x6 only when T1 has locks on all sites that are
up and that contain x6.
dump() gives the committed values of all copies of all variables at all
sites, sorted per site.
dump(i) gives the committed values of all copies of all variables at site i.
dump(xj) gives the committed values of all copies of variable xj at all
sites.
end(T1) causes your system to report whether T1 can commit.
fail(6) says site 6 fails. (This is not issued by a transaction, but is just
an event that the tester will execute.)
recover(7) says site 7 recovers. (Again, a tester-caused event) We discuss
this further below.
A newline means time advances by one. A semicolon is a separator for
co-temporous events.
Example (partial script with six steps in which transactions T1 commits,
and one of T3 and T4 may commit)
begin(T1)
begin(T2)
begin(T3)
W(T1, x1,5); W(T3, x2,32)
W(T2, x1,17); — will cause T2 to die because it cannot wait for an older
lock
end(T1); begin(T4)
W(T4, x4,35); W(T3, x5,21)
W(T4,x2,21); W(T3,x4,23) — T4 will die, freeing the lock on x4 allowing
T3 to finish
Design
Your program should consist of two parts: a single transaction manager
that translates read and write requests on variables to read and write re-
quests on copies using the available copy algorithm described in the notes.
The transaction manager never fails. (Having a single global transaction
manager that never fails is a simplification of reality, but it is not too hard
to get rid of that assumption by using a shared disk configuration.)
If the TM requests a read for transaction T and cannot get it due to
failure, the TM should try another site (all in the same step). If no relevant
site is available, then T must wait. This applies to read-only transactions
as well which must have access to the latest version of each variable before
the transaction begins. T may also have to wait for conflicting locks (if
allowed by the deadlock avoidance protocol). Thus the TM may accumulate
an input command for T and will try it on the next tick (time moment).
As mentioned above, while T is blocked (whether waiting for a lock to be
released or a failure to be cleared), our test files will emit no no operations
for T so the buffer size for messages from any single transaction can be of
size 1.
If a site fails and recovers, the DM would normally perform local recovery
first (perhaps by asking the TM about transactions that the DM holds
pre-committed but not yet committed), but this is unnecessary since, in the
simulation model, commits are atomic with respect to failures. Therefore,
all non-replicated variables are available for reads and writes. Regarding
replicated variables, the site makes them available for writing, but not reading.
In fact, reads will not be allowed at recovered sites until a committed
write takes place (see lecture notes on recovery when using the available
copies algorithm).
During execution, your program should say which transactions commit
and which abort and why. For debugging purposes you should implement
(for your own sake) a command like querystate() which will give the state
of each DM and the TM as well as the data distribution and data values.
Finally, each read that occurs should show the value read.
