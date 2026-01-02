import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { TabParamList, FeedStackParamList, NetworkStackParamList, MessagesStackParamList, NotificationsStackParamList, ProfileStackParamList } from './types';
import { FeedScreen } from '../screens/FeedScreen';
import { CreatePostScreen } from '../screens/CreatePostScreen';
import { ProfileScreen } from '../screens/ProfileScreen';
import { EditProfileScreen } from '../screens/EditProfileScreen';
import { ConnectionsScreen } from '../screens/ConnectionsScreen';
import { ConnectionRequestsScreen } from '../screens/ConnectionRequestsScreen';
import { NetworkScreen } from '../screens/NetworkScreen';
import { MessagesScreen } from '../screens/MessagesScreen';
import { NotificationsScreen } from '../screens/NotificationsScreen';
import { theme } from '../theme';

const Tab = createBottomTabNavigator<TabParamList>();
const FeedStack = createNativeStackNavigator<FeedStackParamList>();
const NetworkStack = createNativeStackNavigator<NetworkStackParamList>();
const MessagesStack = createNativeStackNavigator<MessagesStackParamList>();
const NotificationsStack = createNativeStackNavigator<NotificationsStackParamList>();
const ProfileStack = createNativeStackNavigator<ProfileStackParamList>();

// Stack Navigators
function FeedNavigator() {
  return (
    <FeedStack.Navigator>
      <FeedStack.Screen
        name="FeedList"
        component={FeedScreen}
        options={{ title: 'Feed' }}
      />
      <FeedStack.Screen
        name="CreatePost"
        component={CreatePostScreen}
        options={{
          title: 'Create Post',
          presentation: 'modal'
        }}
      />
      <FeedStack.Screen
        name="UserProfile"
        component={ProfileScreen}
        options={{ title: 'Profile' }}
      />
    </FeedStack.Navigator>
  );
}

function NetworkNavigator() {
  return (
    <NetworkStack.Navigator>
      <NetworkStack.Screen
        name="NetworkList"
        component={NetworkScreen}
        options={{ title: 'Network' }}
      />
      <NetworkStack.Screen
        name="ConnectionRequests"
        component={ConnectionRequestsScreen}
        options={{ title: 'Connection Requests' }}
      />
      <NetworkStack.Screen
        name="UserProfile"
        component={ProfileScreen}
        options={{ title: 'Profile' }}
      />
    </NetworkStack.Navigator>
  );
}

function MessagesNavigator() {
  return (
    <MessagesStack.Navigator>
      <MessagesStack.Screen
        name="MessagesList"
        component={MessagesScreen}
        options={{ title: 'Messages' }}
      />
    </MessagesStack.Navigator>
  );
}

function NotificationsNavigator() {
  return (
    <NotificationsStack.Navigator>
      <NotificationsStack.Screen
        name="NotificationsList"
        component={NotificationsScreen}
        options={{ title: 'Notifications' }}
      />
    </NotificationsStack.Navigator>
  );
}

function ProfileNavigator() {
  return (
    <ProfileStack.Navigator>
      <ProfileStack.Screen
        name="ProfileView"
        component={ProfileScreen}
        options={{ title: 'Profile' }}
      />
      <ProfileStack.Screen
        name="EditProfile"
        component={EditProfileScreen}
        options={{ title: 'Edit Profile' }}
      />
      <ProfileStack.Screen
        name="Connections"
        component={ConnectionsScreen}
        options={{ title: 'Connections' }}
      />
    </ProfileStack.Navigator>
  );
}

// Tab Navigator
export function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: theme.colors.primary,
        tabBarInactiveTintColor: '#64748B',
        tabBarStyle: {
          borderTopColor: '#E2E8F0',
          borderTopWidth: 1,
        },
      }}
    >
      <Tab.Screen
        name="FeedTab"
        component={FeedNavigator}
        options={{
          tabBarLabel: 'Feed',
          tabBarIcon: ({ color, size }) => (
            <Icon name="home" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="NetworkTab"
        component={NetworkNavigator}
        options={{
          tabBarLabel: 'Network',
          tabBarIcon: ({ color, size }) => (
            <Icon name="account-group" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="MessagesTab"
        component={MessagesNavigator}
        options={{
          tabBarLabel: 'Messages',
          tabBarIcon: ({ color, size }) => (
            <Icon name="message" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="NotificationsTab"
        component={NotificationsNavigator}
        options={{
          tabBarLabel: 'Notifications',
          tabBarIcon: ({ color, size }) => (
            <Icon name="bell" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="ProfileTab"
        component={ProfileNavigator}
        options={{
          tabBarLabel: 'Profile',
          tabBarIcon: ({ color, size }) => (
            <Icon name="account" size={size} color={color} />
          ),
        }}
      />
    </Tab.Navigator>
  );
}
