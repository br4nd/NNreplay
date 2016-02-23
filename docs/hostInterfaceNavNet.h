#ifndef __rcrmHostInterfaceNavNet_h
#define __rcrmHostInterfaceNavNet_h

#include "hostInterfaceCommon.h"

// Maximum number of static location definitions
#define NAVNET_MAX_LOCATION_MAP_ENTRIES		(60)

// Maximum number of dynamically-updated location reports
#define NAVNET_MAX_LOCATION_DB_ENTRIES		(32)

// Max length of solver debug message buffer
#define NAVNET_INTERNAL_DEBUG_MSG_MAX_LEN	(1400)

///////////////////////////////////////
//
// Message types
//

// REQUEST messages are sent by the host to the embedded application.
// CONFIRM messages are sent by the embedded application to the host in response to REQUEST messages.
// INFO messages are sent automatically by the embedded application to the host when various events occur.
#define NAVNET_MSG_TYPE_REQUEST			(0x5000)
#define NAVNET_MSG_TYPE_CONFIRM			(0x5100)
#define NAVNET_MSG_TYPE_INFO			(0x5200)


///////////////////////////////////////
//
// Host <-> Embedded conversation messages
//

// Set configuration
#define NAVNET_SET_CONFIG_REQUEST					(NAVNET_MSG_TYPE_REQUEST + 1)
#define NAVNET_SET_CONFIG_CONFIRM					(NAVNET_MSG_TYPE_CONFIRM + 1)

// Get configuration
#define NAVNET_GET_CONFIG_REQUEST					(NAVNET_MSG_TYPE_REQUEST + 2)
#define NAVNET_GET_CONFIG_CONFIRM					(NAVNET_MSG_TYPE_CONFIRM + 2)

// Set local NavNet mode
#define NAVNET_SET_MODE_REQUEST						(NAVNET_MSG_TYPE_REQUEST + 3)
#define NAVNET_SET_MODE_CONFIRM						(NAVNET_MSG_TYPE_CONFIRM + 3)

// Get local NavNet mode
#define NAVNET_GET_MODE_REQUEST						(NAVNET_MSG_TYPE_REQUEST + 4)
#define NAVNET_GET_MODE_CONFIRM						(NAVNET_MSG_TYPE_CONFIRM + 4)

// Set location map (the static definitions of locations)
#define NAVNET_SET_LOCATION_MAP_REQUEST				(NAVNET_MSG_TYPE_REQUEST + 5)
#define NAVNET_SET_LOCATION_MAP_CONFIRM				(NAVNET_MSG_TYPE_REQUEST + 5)

// Get static location map
#define NAVNET_GET_LOCATION_MAP_REQUEST				(NAVNET_MSG_TYPE_REQUEST + 6)
#define NAVNET_GET_LOCATION_MAP_CONFIRM				(NAVNET_MSG_TYPE_REQUEST + 6)

// Get location database (the dynamically-computed database of tracked locations)
#define NAVNET_GET_LOCATION_DB_REQUEST				(NAVNET_MSG_TYPE_REQUEST + 7)
#define NAVNET_GET_LOCATION_DB_CONFIRM				(NAVNET_MSG_TYPE_REQUEST + 7)

// Get individual node location from the location database
#define NAVNET_GET_NODE_LOCATION_REQUEST			(NAVNET_MSG_TYPE_REQUEST + 8)
#define NAVNET_GET_NODE_LOCATION_CONFIRM			(NAVNET_MSG_TYPE_CONFIRM + 8)

///////////////////////////////////////
//
// Embedded -> Host info messages
//

// Location report from local radio
#define NAVNET_LOCATION_INFO						(NAVNET_MSG_TYPE_INFO + 1)

// Simplified location report heard from a remote radio and forwarded up to the host
#define NAVNET_ECHOED_LOCATION_INFO					(NAVNET_MSG_TYPE_INFO + 2)

// Full location report heard from a remote radio and forwarded up to the host
#define NAVNET_ECHOED_LOCATION_EX_INFO				(NAVNET_MSG_TYPE_INFO + 3)

// Auto-sent version of NAVNET_GET_LOCATION_DB_CONFIRM
#define NAVNET_LOCATION_DB_INFO						(NAVNET_MSG_TYPE_INFO + 4)

// Message for passing NavNet internal debug info up to the host
#define NAVNET_INTERNAL_DEBUG_INFO					(NAVNET_MSG_TYPE_INFO + 5)

// Informs the host that a broadcasted NavNet control message (mode or location map change) has been acknowledged by a particular neighbor
#define NAVNET_OTA_ACK_INFO							(NAVNET_MSG_TYPE_INFO + 6)

// Informs host that an over-the-air mode change command has taken effect
#define NAVNET_OTA_MODE_CHANGE_INFO					(NAVNET_MSG_TYPE_INFO + 7)

// Informs host that an over-the-air location map update command has taken effect
#define NAVNET_OTA_LOCATION_MAP_CHANGE_INFO			(NAVNET_MSG_TYPE_INFO + 8)


///////////////////////////////////////
//
// Flags, etc.
//

// NavNet modes

#define NAVNET_MODE_IDLE				(0)
#define NAVNET_MODE_AUTOSURVEY			(1)		// Currently unimplemented
#define NAVNET_MODE_TRACKING			(2)


// Flags for NavNet configuration

// Enable sending (local node) location infos to host upon location updates
#define NAVNET_CONFIG_FLAG_LOCATIONINFO_REPORT_MASK			(0x3)
#define NAVNET_CONFIG_FLAG_LOCATIONINFO_REPORT_NONE			(0x0)
#define NAVNET_CONFIG_FLAG_LOCATIONINFO_REPORT_SUCCESSFUL	(0x1)
#define NAVNET_CONFIG_FLAG_LOCATIONINFO_REPORT_ALL			(0x2)

// Range info reporting flags. Small vs. Full selection is defined in the RCM config.
#define NAVNET_CONFIG_FLAG_RANGEINFO_MASK					(0xc)
#define NAVNET_CONFIG_FLAG_RANGEINFO_REPORT_NONE			(0x0)
#define NAVNET_CONFIG_FLAG_RANGEINFO_REPORT_SUCCESSFUL		(0x4)
#define NAVNET_CONFIG_FLAG_RANGEINFO_REPORT_ALL				(0x8)

// Report heard echoed location messages to the host
#define NAVNET_CONFIG_FLAG_ELL_REPORT						(0x10)

// Report heard echoed range messages to the host
#define NAVNET_CONFIG_FLAG_ELR_REPORT						(0x20)

// Enable autosending the location database at a specified interval,
// similar to RangeNet's ability to autosend the neighbor database.
#define NAVNET_CONFIG_FLAG_AUTOSEND_LDB						(0x40)

// Enables the NavNet Range Target Prioritizer (instead of the RangeNet target prioritizer)
// The NavNet RTP uses knowledge of node locations to choose an optimum range target.
#define NAVNET_CONFIG_FLAG_USE_NAVNET_RTP					(0x80)

// Enables sending of solver debug messages
#define NAVNET_CONFIG_FLAG_SEND_INTERNAL_DEBUG_MSGS			(0x100)


// Fixed axis flags - for when a unit's coordinate(s) are fixed or predefined
#define NAVNET_X_AXIS_FIXED			(1 << 0)
#define NAVNET_Y_AXIS_FIXED			(1 << 1)
#define NAVNET_Z_AXIS_FIXED			(1 << 2)


// Z hemisphere flags
#define NAVNET_Z_HEMISPHERE_FLOAT			(0)
#define NAVNET_Z_HEMISPHERE_ABOVE			(1)
#define NAVNET_Z_HEMISPHERE_BELOW			(2)

// Node types

// Mobile unit
#define NAVNET_NODE_TYPE_MOBILE				(0)

// Generic anchor
#define NAVNET_NODE_TYPE_ANCHOR_GENERIC		(1)

// Anchor defined as the origin (X and Y are 0)
#define NAVNET_NODE_TYPE_ANCHOR_ORIGIN		(2)

// Anchor defined as being along the positive X axis
#define NAVNET_NODE_TYPE_ANCHOR_POSX		(3)

// Anchor defined as being along the negative X axis
#define NAVNET_NODE_TYPE_ANCHOR_NEGX		(4)

// Anchor defined as being along the positive Y axis
#define NAVNET_NODE_TYPE_ANCHOR_POSY		(5)

// Anchor defined as being along the negative Y axis
#define NAVNET_NODE_TYPE_ANCHOR_NEGY		(6)

// Anchor defined as being along the Z axis (positive vs. negative constraints are set elsewhere)
#define NAVNET_NODE_TYPE_ANCHOR_Z			(7)

#define NAVNET_NODE_TYPE_ANCHOR_MIN			NAVNET_NODE_TYPE_ANCHOR_GENERIC
#define NAVNET_NODE_TYPE_ANCHOR_MAX			NAVNET_NODE_TYPE_ANCHOR_Z


// Flags for handling echoed locations and ranges

// Echo Last Location OTA flags masks
#define NAVNET_LOC_FLAG_ELL_OTA_MASK			(0x3)
// Send Echo Last Location over the air. Mutually exclusive with NAVNET_LOC_FLAG_ELL_EX_OTA.
#define NAVNET_LOC_FLAG_ELL_OTA					(0x1)
// Send extended Echo Last Location over the air. Mutually exclusive with NAVNET_LOC_FLAG_ELL_OTA.
#define NAVNET_LOC_FLAG_ELL_EX_OTA				(0x2)

// Echo Last Range OTA flags masks
#define NAVNET_LOC_FLAG_ELR_MASK				(0x4)
// Send Echo Last Range over the air
#define NAVNET_LOC_FLAG_ELR_OTA					(0x4)



// Location database sort codes and filter flags
// Sort codes are in the lower bits and filter flags are in the upper bits.
// If both mobiles and anchors are included, the location DB is sorted with mobiles first before applying the selected sort.

// Sort by node ID (default)
#define NAVNET_LOC_DB_SORT_NODE_ID				(0)
// Sort by distance, closest first
#define NAVNET_LOC_DB_SORT_DISTANCE				(1)


// Include mobiles (default set)
#define NAVNET_LOC_DB_FILTER_INCLUDE_MOBILES	(0x80)
// Include anchors (default not set)
#define NAVNET_LOC_DB_FILTER_INCLUDE_ANCHORS	(0x40)

// Solver stages - indicate the level to which the solver has progressed.
// In normal operation the solver will be running in NAVNET_SOLVER_STAGE_KALMAN, but during initialization stages it will be one of the other values.

// Indicates that the solver has been initialized (most likely from the Location Map)
#define NAVNET_SOLVER_STAGE_INITIALIZED			(0)
// Indicates the solver is in Geometric (Nonlinear Least Squares) initialization mode.
#define NAVNET_SOLVER_STAGE_NLS					(1)
// Indicates the solver is running in Kalman solver init mode (transition from NLS to running the regular Kalman solver)
#define NAVNET_SOLVER_STAGE_KALMAN_INIT			(2)
// Indicates the solver is running in full Kalman solver mode
#define NAVNET_SOLVER_STAGE_KALMAN					(3)


// Error codes indicating why the most recent range did not produce a new position.

// Indicates no error occurred.
#define NAVNET_SOLVER_ERROR_NONE						(0)

// The range did not pass range filters.
#define NAVNET_SOLVER_ERROR_RANGE_ERROR					(128)

// There are not enough or new enough ranges to initialize the nonlinear least squares solver.
#define NAVNET_SOLVER_ERROR_NLS_INSUFFICIENT_RANGES		(129)
// The three anchors available fail the geometry filter test to initialize the NLS solver.
#define NAVNET_SOLVER_ERROR_NLS_ERROR_GEOMETRY			(130)
// The NLS solver failed to converge.
#define NAVNET_SOLVER_ERROR_NLS_ERROR_CONVERGENCE		(131)

// A Kalman update was not used since its error estimate was too large.
#define NAVNET_SOLVER_ERROR_KALMAN_ERR_EST_TOO_LARGE	(132)

// Generic error code
#define NAVNET_SOLVER_ERROR_GENERIC_ERROR				(255)

///////////////////////////////////////
//
// Message struct definitions
//

typedef struct
{
	// NavNet behavior flags
	rcrm_uint16_t flags;
	
	// NavNet mode to use upon bootup
	rcrm_uint8_t bootMode;

	// Autosent location database sort code and filter flags
	rcrm_uint8_t autosendLocDbSortAndFilter;
	
	// How often to send the location database (if the relevant autosend flag is enabled).
	rcrm_uint16_t autosendLocDbIntervalMs;

	// Minimum range error estimate, in mm.
	// Ranges with error estimates LESS than this are rejected on the basis that we don't trust the value.
	// Set to 0 to disable.
	rcrm_uint16_t solverMinREE;
	
	// Maximum range error estimate, in mm, before a range is rejected.
	// Set to 0 to disable.
	rcrm_uint16_t solverMaxREE;

	// Maximum location error estimate of local solution, in mm, before RTP reverts to ALOHA RTP (if NN RTP is enabled)
	rcrm_uint16_t rtpMaxLEE;
	
	// Kalman solver parameter overrides (set to 0 to use defaults)
	
	// Range measurement weight, multiplied by 1000 (e.g. for a weight of 0.1, use 100)
	rcrm_uint16_t kalmanSigmaRange;
	
	// Kalman model weight, multiplied by 1000 (e.g. for a weight of 0.1, use 100)
	rcrm_uint16_t kalmanSigmaAccel;
	
	// Minimum triangle score, in mm.
	rcrm_uint16_t minTriangleScore;
	
	rcrm_uint16_t reserved;
} navNetConfiguration;

typedef struct
{
	rcrm_uint32_t nodeId;
	
	// Anchor, Mobile, etc.
	rcrm_uint8_t nodeType;

	// Bit 0: X axis
	// Bit 1: Y axis
	// Bit 2: Z axis
	// Bits 4, 5 (upper nibble): Z axis hemisphere (above, below, float)
	rcrm_uint8_t axisDefinitions;
	
	// Echo location and range flags, etc.
	rcrm_uint8_t flags;

	rcrm_uint8_t reserved1;
	
	rcrm_uint16_t reserved2;

	// Beacon transmit interval in milliseconds. Set to 0 to use ACC.
	rcrm_uint16_t beaconIntervalMs;
	
	struct
	{
		rcrm_int32_t x;
		rcrm_int32_t y;
		rcrm_int32_t z;
	} loc_mm;
} navNetLocationDefinition;

typedef struct
{
	rcrm_uint32_t nodeId;
	
	// Anchor, Mobile, etc.
	rcrm_uint8_t nodeType;

	rcrm_uint8_t solverStage;
	
	rcrm_uint8_t solverErrorCode;
	
	// Bit 0: X axis fixed
	// Bit 1: Y axis fixed
	// Bit 2: Z axis fixed
	// Bits 4, 5 (upper nibble): Z hemisphere (above, below, float)
	rcrm_uint8_t axisDefinitions;
	
	rcrm_uint8_t reserved1[2];
	
	// Location error estimate in mm
	rcrm_uint16_t locationErrorEstimateMm;
	
	rcrm_uint32_t timestampMs;
	
	struct
	{
		rcrm_int32_t x;
		rcrm_int32_t y;
		rcrm_int32_t z;
	} loc_mm;
	
	struct
	{
		rcrm_uint16_t var_x;
		rcrm_uint16_t var_y;
		rcrm_uint16_t var_z;

		rcrm_uint16_t covar_xy;
		rcrm_uint16_t covar_xz;
		rcrm_uint16_t covar_yz;
	} kalman_state;
} navNetLocationReport;


///////////////////////////////////////
//
// Host <-> NavNet conversation messages
//

typedef struct
{
	// set to NAVNET_SET_CONFIG_REQUEST
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;

	navNetConfiguration config;

	// Set to indicate settings should persist across radio reboots
	rcrm_uint8_t persistFlag;
	
	rcrm_uint8_t reserved[3];
} navNetMsg_SetConfigRequest;

typedef struct
{
	// set to NAVNET_SET_CONFIG_CONFIRM
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;

	// status code
	rcrm_uint32_t status;
} navNetMsg_SetConfigConfirm;


typedef struct
{
	// set to NAVNET_GET_CONFIG_REQUEST
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;
} navNetMsg_GetConfigRequest;

typedef struct
{
	// set to NAVNET_GET_CONFIG_CONFIRM
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;

	navNetConfiguration config;

	// milliseconds since radio boot
	rcrm_uint32_t timestamp;

	// status code
	rcrm_uint32_t status;
} navNetMsg_GetConfigConfirm;


typedef struct
{
	// set to NAVNET_SET_MODE_REQUEST
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;
	
	// Requested NavNet mode.
	rcrm_uint8_t mode;
	
	// Set to nonzero to indicate the mode change should be broadcast over UWB.
	rcrm_uint8_t broadcastFlag;
	
	rcrm_uint8_t reserved[2];
} navNetMsg_SetModeRequest;

typedef struct
{
	// set to NAVNET_SET_MODE_CONFIRM
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;
	
	// New NavNet mode
	rcrm_uint8_t mode;
	
	rcrm_uint8_t reserved[3];

	rcrm_uint32_t status;
} navNetMsg_SetModeConfirm;

typedef struct
{
	// set to NAVNET_GET_MODE_REQUEST
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;
} navNetMsg_GetModeRequest;

typedef struct
{
	// set to NAVNET_GET_MODE_CONFIRM
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;
	
	// Current NavNet mode
	rcrm_uint8_t mode;
	
	rcrm_uint8_t reserved[3];
} navNetMsg_GetModeConfirm;

typedef struct
{
	// set to NAVNET_SET_LOCATION_MAP_REQUEST
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;
	
	// Reserved for aligment and future growth
	rcrm_uint8_t reserved;

	// Set to nonzero to indicate the new location map should be broadcast over UWB.
	rcrm_uint8_t broadcastFlag;

	// Number of entries in this variable-length message
	rcrm_uint8_t numLocations;

	// Set to non-zero to indicate settings should persist across radio reboots
	rcrm_uint8_t persistFlag;
	
	// The static location definitions.
	// Only the first numLocations need be included in this variable-length message.
	navNetLocationDefinition locations[NAVNET_MAX_LOCATION_MAP_ENTRIES];
} navNetMsg_SetLocationMapRequest;

typedef struct
{
	// set to NAVNET_SET_LOCATION_MAP_CONFIRM
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;

	// status code
	rcrm_uint32_t status;
} navNetMsg_SetLocationMapConfirm;


typedef struct
{
	// set to NAVNET_GET_LOCATION_MAP_REQUEST
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;
} navNetMsg_GetLocationMapRequest;

typedef struct
{
	// set to NAVNET_GET_LOCATION_MAP_CONFIRM
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;
	
	// Number of location entries in this variable-length packet
	rcrm_uint8_t numLocations;
	
	rcrm_uint8_t reserved[3];

	// status code
	rcrm_uint32_t status;

	// The static location definitions.
	// Only the first numLocations are included in this variable-length message.
	navNetLocationDefinition locations[NAVNET_MAX_LOCATION_MAP_ENTRIES];
} navNetMsg_GetLocationMapConfirm;

typedef struct
{
	// set to NAVNET_GET_LOCATION_DB_REQUEST
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;
	
	rcrm_uint8_t maxNeighborEntries;
	rcrm_uint8_t sortAndFilter;
	
	rcrm_uint16_t reserved;
} navNetMsg_GetLocationDBRequest;

typedef struct
{
	// set to NAVNET_GET_LOCATION_DB_CONFIRM or NAVNET_LOCATION_DB_INFO
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;

	// Number of location entries in this variable-length message
	rcrm_uint8_t numEntries;

	// Sort and filter used
	rcrm_uint8_t sortAndFilter;

	rcrm_uint16_t reserved;

	rcrm_uint32_t timestamp;

	rcrm_uint32_t status;

	navNetLocationReport locations[NAVNET_MAX_LOCATION_DB_ENTRIES];
} navNetMsg_GetLocationDBConfirm;

typedef struct
{
	// set to NAVNET_GET_NODE_LOCATION_REQUEST
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;

	// Node ID. Set to 0 (or the local radio's node ID) to get the local node location.
	rcrm_uint32_t nodeId;
} navNetMsg_GetNodeLocationRequest;

typedef struct
{
	// set to NAVNET_GET_NODE_LOCATION_CONFIRM
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;

	navNetLocationReport location;
	
	rcrm_uint32_t status;
} navNetMsg_GetNodeLocationConfirm;

///////////////////////////////////////
//
// NavNet -> Host INFO messages
//

typedef struct
{
	// set to NAVNET_LOCATION_INFO
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;

	// Timestamp when this message was sent.
	rcrm_uint32_t timestamp;

	navNetLocationReport location;
} navNetMsg_LocationInfo;

typedef struct
{
	// set to NAVNET_ECHOED_LOCATION_INFO
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;

	// ID of the remote radio
	rcrm_uint32_t nodeId;
	
	// Milliseconds since the remote radio boot at the time of the localization.
	// Used to identify duplicate ELR reports.
	rcrm_uint32_t remoteTimestamp;

	// Location XYZ in mm
	struct
	{
		rcrm_int32_t x;
		rcrm_int32_t y;
		rcrm_int32_t z;
	} loc_mm;
	
	// Location error estimate in mm.
	rcrm_uint16_t leeMm;
	
	rcrm_uint8_t solverStage;
	
	rcrm_uint8_t solverErrorCode;
} navNetMsg_EchoedLocationInfo;

typedef struct
{
	// set to NAVNET_ECHOED_LOCATION_EX_INFO
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;

	navNetLocationReport location;
} navNetMsg_EchoedLocationExInfo;

// Identical to navNetMsg_GetLocationDBConfirm, except auto-sent and with message type NAVNET_LOCATION_DB_INFO
typedef navNetMsg_GetLocationDBConfirm navNetMsg_LocationDBInfo;

typedef struct
{
	// set to NAVNET_OTA_MODE_CHANGE_INFO
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;

	// New NavNet mode
	rcrm_uint8_t newMode;

	// Reserved for alignment
	rcrm_uint8_t reserved[3];

	// Node ID of the radio that commanded the mode change
	// (this is the radio connected to the host that initiated the mode change)
	rcrm_uint32_t sourceNodeId;

	// Node ID of the radio the mode change command was heard from
	// (may be different from sourceNodeId due to routing over multiple hops)
	rcrm_uint32_t routeNodeId;
} navNetMsg_OTAModeChangeInfo;

typedef struct
{
	// set to NAVNET_OTA_LOCATION_MAP_CHANGE_INFO
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;

	// Persist flag
	rcrm_uint8_t persistFlag;

	// Reserved for alignment
	rcrm_uint8_t reserved[3];

	// Node ID of the radio that commanded the location map change
	// (this is the radio connected to the host that initiated the location map change)
	rcrm_uint32_t sourceNodeId;

	// Node ID of the radio the location map change command was heard from
	// (may be different from sourceNodeId due to routing over multiple hops)
	rcrm_uint32_t routeNodeId;
} navNetMsg_OTALocationMapChangeInfo;

typedef struct
{
	// set to NAVNET_INTERNAL_DEBUG_INFO
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;
	
	// Millisecond timestamp of message.
	rcrm_uint32_t timestampMillisecond;
	
	// Microsecond timestamp of message.
	rcrm_uint32_t timestampMicrosecond;
	
	// Variable-length custom message generated by the solver
	char msg[NAVNET_INTERNAL_DEBUG_MSG_MAX_LEN];
} navNetMsg_InternalDebugInfo;

typedef struct
{
	// set to NAVNET_OTA_ACK_INFO
	rcrm_uint16_t msgType;
	// identifier to correlate requests with confirms
	rcrm_uint16_t msgId;
	
	// Node ID of the acknowledging neighbor
	rcrm_uint32_t nodeId;
	
	// Message type of the OTA command that was acknowledged.
	// Will be NAVNET_SET_MODE_REQUEST or NAVNET_SET_LOCATION_MAP_REQUEST.
	rcrm_uint16_t cmdMsgType;
	
	rcrm_uint16_t reserved;
} navNetMsg_OTAAckInfo;

#endif	// #ifdef __rcrmHostInterfaceNavNet_h
 
