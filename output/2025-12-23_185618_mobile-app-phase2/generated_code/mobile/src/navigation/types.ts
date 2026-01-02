import { NavigatorScreenParams } from '@react-navigation/native';

// Auth Stack
export type AuthStackParamList = {
  Login: undefined;
  Signup: undefined;
  Onboarding: undefined;
};

// Feed Stack
export type FeedStackParamList = {
  FeedList: undefined;
  PostDetail: { postId: string };
  CreatePost: undefined;
  UserProfile: { userId: string };
};

// Network Stack
export type NetworkStackParamList = {
  NetworkList: undefined;
  ConnectionRequests: undefined;
  UserProfile: { userId: string };
};

// Messages Stack
export type MessagesStackParamList = {
  MessagesList: undefined;
  Chat: { conversationId: string; userName: string };
};

// Notifications Stack
export type NotificationsStackParamList = {
  NotificationsList: undefined;
};

// Profile Stack
export type ProfileStackParamList = {
  ProfileView: undefined;
  EditProfile: undefined;
  Connections: undefined;
  Settings: undefined;
};

// Tab Navigator
export type TabParamList = {
  FeedTab: NavigatorScreenParams<FeedStackParamList>;
  NetworkTab: NavigatorScreenParams<NetworkStackParamList>;
  MessagesTab: NavigatorScreenParams<MessagesStackParamList>;
  NotificationsTab: NavigatorScreenParams<NotificationsStackParamList>;
  ProfileTab: NavigatorScreenParams<ProfileStackParamList>;
};

// Root Navigator
export type RootStackParamList = {
  Auth: NavigatorScreenParams<AuthStackParamList>;
  Main: NavigatorScreenParams<TabParamList>;
};

declare global {
  namespace ReactNavigation {
    interface RootParamList extends RootStackParamList {}
  }
}
