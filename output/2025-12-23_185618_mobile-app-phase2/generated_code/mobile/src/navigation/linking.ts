import { LinkingOptions } from '@react-navigation/native';
import { RootStackParamList } from './types';

export const linking: LinkingOptions<RootStackParamList> = {
  prefixes: ['trustlink://', 'https://trustlink.app'],
  config: {
    screens: {
      Auth: {
        screens: {
          Login: 'login',
          Signup: 'signup',
          Onboarding: 'onboarding',
        },
      },
      Main: {
        screens: {
          FeedTab: {
            screens: {
              FeedList: 'feed',
              PostDetail: 'post/:postId',
              CreatePost: 'create-post',
              UserProfile: 'profile/:userId',
            },
          },
          NetworkTab: {
            screens: {
              NetworkList: 'network',
              ConnectionRequests: 'connection-requests',
              UserProfile: 'profile/:userId',
            },
          },
          MessagesTab: {
            screens: {
              MessagesList: 'messages',
              Chat: 'chat/:conversationId',
            },
          },
          NotificationsTab: {
            screens: {
              NotificationsList: 'notifications',
            },
          },
          ProfileTab: {
            screens: {
              ProfileView: 'my-profile',
              EditProfile: 'edit-profile',
              Connections: 'connections',
              Settings: 'settings',
            },
          },
        },
      },
    },
  },
};
